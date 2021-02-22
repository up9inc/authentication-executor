from authentication_executor.authenticators.base_authenticator import AuthenticationPayload, AuthenticationResult, \
    AuthenticationStatus, AuthSpecABC, \
    BaseAuthenticatorABC


class OAuth2AuthenticatorSpec(AuthSpecABC):
    def __init__(self, grant_type, access_token_url, scope, client_id, client_secret, username, password, auth_url, state, callback_url, authenticate_in_headers):
        self.grant_type = grant_type
        self.access_token_url = access_token_url
        self.scope = scope
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.auth_url = auth_url
        self.state = state
        self.callback_url = callback_url
        self.authenticate_in_headers = authenticate_in_headers

    @staticmethod
    def from_dict(spec: dict):
        return OAuth2AuthenticatorSpec(spec["grantType"], spec['accessTokenUrl'], spec['scope'],
                                       spec['clientId'], spec['clientSecret'], spec.get('username'),
                                       spec.get('password'), spec.get('authUrl'), spec.get('state'),
                                       spec.get('callbackUrl'), spec.get('authInHeaders'))


class OAuth2Authenticator(BaseAuthenticatorABC):
    spec_class = OAuth2AuthenticatorSpec

    def execute(self) -> AuthenticationResult:

        if self.execution_spec.grant_type == 'client_credentials':
            pass # basic call to access_token_url with proper body
        elif self.execution_spec.grant_type == 'password':
            pass # basic call to access_token_url with proper body
        elif self.execution_spec.grant_type == 'authorization_code':
            pass # call auth_url, take code then send it to access_token_url then get token response
        else:
            pass # NOT SUPPORTED EXCEPTION

        return AuthenticationResult(
            AuthenticationStatus.SUCCESS,
            AuthenticationPayload(
                headers=None
            ),
            None,
            []
        )
