from functools import wraps
import uuid

def fix_qid(expects='hex', param_name='questionnaire_id'):
    def wrapper_outer(func):
        @wraps(func)
        def wrapper_inner(*args, **kwargs):
            if param_name in kwargs:
                if expects == 'hex':
                    kwargs[param_name] = uuid.UUID(kwargs[param_name]).hex
                elif expects == 'string':
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
        q_id = qq[0]
        q_version = qq[1]

    return to_qidentity(q_id, q_version)