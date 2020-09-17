import unittest

import base64

valid_custom_code_1 = b"def custom_auth() -> AuthenticationPayload:\n" \
        b"\tprint('debugTest')\n" \
        b"\tresp = requests.get('http://google.com')\n" \
        b"\treturn AuthenticationPayload(headers={'Auth':'1'})"

code2 = b"def custom_auth() -> AuthenticationPayload:\n" \
        b"\tresp = requests.get('http://google.com')\n" \
        b"\treturn AuthenticationPayload(headers={'Auth':'2'})"

code3 = b"def custom_auth() -> AuthenticationPayload:\n" \
        b"\ttarget.additional_headers()"

code4 = b"def koko():"

configs_1 = {
    "XXX_ZZZ": {
        "type": "customCode",
        "spec": {
            "customCode": base64.b64encode(valid_custom_code_1)
        }
    }
}

configs = [
    # valid_custom_code_spec_1,
    {
        "type": "customCode",
        "spec": {
            "customCode": base64.b64encode(code2)
        }
    },
    {
        "type": "request",
        "spec": {
            "url": "http://google.com/token"
        }
    }
]