import uuid
from datetime import datetime
from functools import wraps
from typing import List, Optional, Type, TypeVar, Union

from sgqlc.types import Input

from .exceptions import IncompleteQuestionnaireIdError


def fix_qid(expects: dict = {'questionnaire_id': 'hex'}):
    def wrapper_outer(func):
        @wraps(func)
        def wrapper_inner(*args, **kwargs):
            for param_name in expects.keys():
                if param_name in kwargs:
                    if expects[param_name] == 'hex':
                        kwargs[param_name] = uuid.UUID(kwargs[param_name]).hex
                    elif expects[param_name] == 'string':
                        try:
                            kwargs[param_name] = str(uuid.UUID(kwargs[param_name]))
                        except (AttributeError, ValueError):
                            raise ValueError(f"{param_name} expect a valid uuid string")
                    else:
                        raise ValueError('expects should be either hex or string')
            return func(*args, **kwargs)
        return wrapper_inner
    return wrapper_outer


def to_hex(q_id):
    return uuid.UUID(str(q_id)).hex


def to_qidentity(q_id: str, q_version: int) -> str:
    return f"{to_hex(q_id)}${q_version}"


def parse_qidentity(q_identity):
    if type(q_identity) is tuple:
        (q_id, q_version) = q_identity
    else:
        qq = q_identity.split("$")
        try:
            q_id = qq[0]
            q_version = qq[1]
        except IndexError:
            raise(IncompleteQuestionnaireIdError)

    return to_qidentity(q_id, q_version)


def to_pascal(string: str) -> str:
    return "".join(word.capitalize() for word in string.split("_"))


def to_camel(string: str) -> str:
    init, *temp = string.split("_")

    return "".join([init.lower(), *map(str.title, temp)])


def get_properties(obj, types: Optional[list] = None, properties: Optional[list] = None,
                   groups: bool = False, items: bool = True) -> dict:
    ret = {}
    if type(obj).__name__ in ["Group", "QuestionnaireDocument"]:
        if groups:
            ret[obj.public_key.hex] = obj
        for ch in obj.children:
            ret.update(get_properties(ch, types, properties, groups, items))
    elif items:
        type_name = type(obj).__name__
        if not types or type_name in types:
            if properties:
                ret[obj.variable_name] = {p: getattr(obj, p) for p in properties if hasattr(obj, p)}
            else:
                ret[obj.variable_name] = obj
    return ret


InputType = TypeVar("InputType", bound=Input)


def order_object(order_type: Type[InputType], params: Union[dict, list, tuple, str]) -> List[InputType]:
    if type(params) in [list, tuple]:
        d = {}
        for item in params:
            if type(item) is tuple:
                d[item[0]] = item[1]
            elif type(item) is str:
                d[item] = "ASC"
            else:
                raise TypeError("Elements must be either string or tuple")
        params = d
    elif type(params) is not dict:
        raise TypeError("Argument must be dict, list, or tuple")

    return [order_type(**{item[0]: item[1]}) for item in params.items()]


def filter_object(filter_type: Type[InputType], where: Optional[InputType] = None, **kwargs) -> InputType:

    if where and type(where) is not filter_type:
        raise TypeError(f"where parameter must be an object of type {filter_type}")

    fields = [item for item in getattr(filter_type, "__field_names__") if item not in ["and_", "or_"]]
    filter_args = {}
    for key, value in kwargs.items():
        if key not in fields:
            raise KeyError(f"{filter_type} does not contain field {key}")
        field_type = getattr(filter_type, key).type
        if key in ["responsible_name", "supervisor_name"]:
            value = value.lower()
        filter_args[key] = field_type(eq=value)

    if not where:
        return filter_type(**filter_args)
    if filter_args:
        return filter_type(and_=[where, filter_type(**filter_args)])
    else:
        return where


def parse_date(date_string: str) -> Union[datetime, None]:
    if date_string:
        return datetime.strptime(f"{date_string[:24]}+0000", "%Y-%m-%dT%H:%M:%S.%f%z")
