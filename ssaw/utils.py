import uuid

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