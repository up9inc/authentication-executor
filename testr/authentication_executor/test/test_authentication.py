import unittest

import base64

from testr.authentication_executor.authenticator import Authenticator
from testr.authentication_executor.authenticators.authenticator_factory import InvalidAuthenticator
from testr.authentication_executor import CustomCodeRuntimeError, InvalidCodeError

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


class AuthenticationTests(unittest.TestCase):
    def test_invalid_spec(self):
        try:
            Authenticator.verify_config({
                "type": "xxx",
                "spec": ""
            })
        except InvalidAuthenticator:
            return
        except Exception:
            pass
        self.fail("Did not raise InvalidAuthenticator")

    def test_mutiple(self):
        results = Authenticator.execute(configs, {})
        print(results.json)
        self.assertEqual(results['entityPayloads'][1]['headers'], {'Auth': '2'})

    def _test_verify(self):
        result = Authenticator.verify_config(configs[2])

    def test_custom_code_runtime_error(self):
        try:
            result = Authenticator.verify_config({
                "type": "customCode",
                "spec": {
                    "customCode":
                        base64.b64encode(code3)
                }
            })
        except CustomCodeRuntimeError:
            return
        except Exception:
            pass
        self.fail("Did not raise CustomCodeRuntimeError")

    def test_custom_code_syntax_error(self):
        try:
            result = Authenticator.verify_config({
                "type": "customCode",
                "spec": {
                    "customCode":
                        base64.b64encode(code4)
                }
            })
        except InvalidCodeError:
            return
        except Exception:
            pass
        self.fail("Did not raise InvalidCodeError")


if __name__ == '__main__':
    unittest.main()
