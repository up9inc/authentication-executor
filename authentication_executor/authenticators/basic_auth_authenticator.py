from authentication_executor.authenticators.base_authenticator import AuthenticationPayload, AuthenticationResult, \
    AuthenticationStatus, AuthSpecABC, \
    BaseAuthenticatorABC
import base64


class BasicAuthAuthenticatorSpec(AuthSpecABC):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def from_dict(spec: dict):
        return BasicAuthAuthenticatorSpec(spec["username"], spec["password"])


class BasicAuthAuthenticator(BaseAuthenticatorABC):
    spec_class = BasicAuthAuthenticatorSpec

    def execute(self) -> AuthenticationResult:
        return AuthenticationResult(
            AuthenticationStatus.SUCCESS,
            AuthenticationPayload(
                headers={
                    "Authorization": "Basic " + base64.b64encode(f'{self.execution_spec.username}:{self.execution_spec.password}'.encode('utf-8')).decode()
                }
            ),
            None,
            []
        )
