from testr.authentication_executor.authenticators.base_authenticator import AuthenticationPayload, AuthenticationResult, \
    AuthenticationStatus, AuthSpecABC, \
    BaseAuthenticatorABC
from testr.authentication_executor.util.request_wrapper import RequestWrapper


# STUB - for testing only for now
class RequestAuthenticatorSpec(AuthSpecABC):
    def __init__(self, url):
        self.url = url

    @staticmethod
    def from_dict(spec: dict):
        return RequestAuthenticatorSpec(spec["url"])


class RequestAuthenticator(BaseAuthenticatorABC):
    spec_class = RequestAuthenticatorSpec

    def execute(self) -> AuthenticationResult:
        requests_session = RequestWrapper().session
        resp = requests_session.get(self.execution_spec.url)
        requests_session.close()
        return AuthenticationResult(
            AuthenticationStatus.SUCCESS,
            AuthenticationPayload(
                headers={
                    "XX": "1"
                }
            ),
            None,
            []
        )
