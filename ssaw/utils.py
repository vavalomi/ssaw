import uuid

def to_qidentity(q_id, q_version):
    return "{}${}".format(uuid.UUID(q_id).hex, q_version)