import uuid
from datetime import datetime
from functools import wraps

from .exceptions import IncompleteQuestionnaireIdError
from .headquarters_schema import headquarters_schema as schema


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


def to_qidentity(q_id, q_version):
    return "{}${}".format(to_hex(q_id), q_version)


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


def to_camel(string: str) -> str:
    return ''.join(word.capitalize() for word in string.split('_'))


def get_properties(obj, types: list = [], properties: list = [], groups: bool = False, items: bool = True) -> dict:
    ret = {}
    if type(obj).__name__ in ["Group", "QuestionnaireDocument"]:
        if groups:
            ret[obj.public_key.hex] = obj
        for ch in obj.children:
            ret.update(get_properties(ch, types, properties, groups, items))
    elif items:
        type_name = type(obj).__name__
        if type_name in types or not types:
            if properties:
                ret[obj.variable_name] = {p: getattr(obj, p) for p in properties if hasattr(obj, p)}
            else:
                ret[obj.variable_name] = obj
    return ret


def order_object(classname: str, params):
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

    return [getattr(schema, classname)(**{item[0]: item[1]}) for item in params.items()]


def filter_object(classname: str, where=None, **kwargs):
    filter_type = getattr(schema, classname)
    if where and type(where) is not filter_type:
        raise TypeError(f"where parameter must be an object of type {classname}")

    fields = [item for item in getattr(filter_type, "__field_names__") if item not in ["and_", "or_"]]
    filter_args = {}
    for key, value in kwargs.items():
        if key not in fields:
            raise KeyError(f"{classname} does not contain field {key}")
        field_type = getattr(getattr(schema, classname), key).type
        if key in ["responsible_name", "supervisor_name"]:
            value = value.lower()
        filter_args[key] = field_type(eq=value)

    if where:
        if filter_args:
            return filter_type(and_=[where, filter_type(**filter_args)])
        else:
            return where
    else:
        if filter_args:
            return filter_type(**filter_args)


def parse_date(date_string: str) -> datetime:
    try:
        return datetime.strptime(f"{date_string}+0000", "%Y-%m-%dT%H:%M:%S.%f%z")
    except (TypeError, ValueError):
        return date_string
