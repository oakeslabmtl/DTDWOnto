import json

ENCODING = "ascii"

def convert_str_to_bool(body):
    if body is None:
        return None
    else:
        return body.decode(ENCODING) == "True"


def encode_json(object):
    return json.dumps(object).encode(ENCODING)


def decode_json(bytes):
    return json.loads(bytes.decode(ENCODING))


def from_ns_to_s(time_ns):
    return time_ns / 1e9


def from_s_to_ns(time_s):
    return int(time_s * 1e9)


def from_s_to_ns_array(time_s):
    ns_floats = time_s * 1e9
    ns_ints = ns_floats.astype(int)
    return ns_ints
