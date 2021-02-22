from authentication_executor.authenticators.base_authenticator import AuthenticationPayload, AuthenticationResult, \
    AuthenticationStatus, AuthSpecABC, \
    BaseAuthenticatorABC


class HeadersAuthenticatorSpec(AuthSpecABC):
    def __init__(self, headers_list):
        self.headers_list = headers_list

    @staticmethod
    def from_dict(spec: dict):
        return HeadersAuthenticatorSpec(spec["headers"])


class HeadersAuthenticator(BaseAuthenticatorABC):
    spec_class = HeadersAuthenticatorSpec

    def execute(self) -> AuthenticationResult:
        headers_dict = {item['key']: item['value'] for item in self.execution_spec.headers_list}
        return AuthenticationResult(
            AuthenticationStatus.SUCCESS,
            AuthenticationPayload(
                headers=headers_dict
            ),
            None,
            []
        )
