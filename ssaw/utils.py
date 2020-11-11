import uuid
from functools import wraps

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
                        kwargs[param_name] = str(uuid.UUID(kwargs[param_name]))
                    else:
                        raise ValueError('expects should be either hex or string')
            return func(*args, **kwargs)
        return wrapper_inner
    return wrapper_outer


def to_hex(q_id):
    return uuid.UUID(q_id).hex


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


def get_variables(obj, tt=[]):
    if hasattr(obj, "children"):
        for ch in obj.children:
            yield from get_variables(ch, tt)
    else:
        type_name = type(obj).__name__
        if type_name in tt or not tt:
            yield obj
