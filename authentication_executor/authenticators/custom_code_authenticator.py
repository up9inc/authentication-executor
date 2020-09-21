import base64
from typing import Optional

from authentication_executor.authenticators.base_authenticator import AuthenticationPayload, AuthenticationResult, \
    AuthenticationStatus, AuthSpecABC, BaseAuthenticatorABC
from authentication_executor.util.request_wrapper import RequestWrapper


def decode_base64_code(base64_code, indent_space_amount):
    decoded = base64.b64decode(base64_code).decode("utf-8")
    indent_spaces = ' ' * indent_space_amount
    return indent_spaces + indent_spaces.join(decoded.splitlines(True))


class CustomCodeAuthSpec(AuthSpecABC):
    @staticmethod
    def from_dict(spec: dict):
        return CustomCodeAuthSpec(spec["customCode"])

    def __init__(self, b64code):
        self.b64code = b64code


# TODO upload HARs on a nonblock thread (but wait for it to end)

class InvalidCodeEncodingError(Exception):
    pass


class InvalidCodeError(Exception):
    pass


class CustomCodeRuntimeError(Exception):
    pass


class CustomCodeAuthenticator(BaseAuthenticatorABC):
    spec_class = CustomCodeAuthSpec

    def execute(self) -> AuthenticationResult:
        global print
        request_wrapper = RequestWrapper()
        requests = request_wrapper.session

        debug_data = []
        _print = print

        def debug_print(str, *args, **kwargs):
            debug_data.append(f'{str}'[:500])
            _print(str, *args, **kwargs)

        authentication: Optional[AuthenticationPayload] = None
        status = AuthenticationStatus.SUCCESS

        try:
            print = debug_print

            try:
                code = decode_base64_code(self.execution_spec.b64code, 0)
            except Exception as e:
                raise InvalidCodeEncodingError(e)

            try:
                # Ensure user function receives both global and local scope.
                # This will cause the function to not actually be defined in this local scope but on the dict instead
                combined_scope_dict = {**globals(), **locals()}
                exec(code, combined_scope_dict)
                compiled_func = combined_scope_dict['custom_auth']
            except Exception as e:
                raise InvalidCodeError(e)

            try:
                authentication = compiled_func()
            except Exception as e:
                raise CustomCodeRuntimeError(e)

        except InvalidCodeEncodingError as e:
            debug_data.append("Unable to decode code")
            debug_data.append(str(e))
            status = AuthenticationStatus.FAIL
        except InvalidCodeError as e:
            debug_data.append("Unable to compile code")
            debug_data.append(str(e))
            status = AuthenticationStatus.FAIL
        except CustomCodeRuntimeError as e:
            debug_data.append("Custom code runtime error")
            debug_data.append(str(e))
            status = AuthenticationStatus.FAIL
        finally:
            print = _print
            requests.close()

        return AuthenticationResult(
            status,
            authentication,
            request_wrapper.to_har(),
            debug_data
        )
