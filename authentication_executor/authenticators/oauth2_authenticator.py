from urllib.parse import urlparse, parse_qs

from authentication_executor.authenticators.base_authenticator import AuthenticationPayload, AuthenticationResult, \
    AuthenticationStatus, AuthSpecABC, \
    BaseAuthenticatorABC
from authentication_executor.util.request_wrapper import RequestWrapper
import base64


def get_without_none_values(dictionary: dict):
    """Returns new dict without None values"""
    return {
        key: value for key, value in dictionary.items() if value is not None
    }


class OAuth2AuthenticatorSpec(AuthSpecABC):
    def __init__(self, grant_type, token_url, scope, client_id, client_secret, username, password, authorization_url, state, callback_url, client_creds_in_headers):
        self.grant_type = grant_type
        self.token_url = token_url
        self.scope = scope
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.authorization_url = authorization_url
        self.state = state
        self.callback_url = callback_url
        self.client_creds_in_headers = client_creds_in_headers

    @staticmethod
    def from_dict(spec: dict):
        return OAuth2AuthenticatorSpec(spec["grantType"], spec['tokenUrl'], spec['scope'],
                                       spec['clientId'], spec['clientSecret'], spec.get('username'),
                                       spec.get('password'), spec.get('authorizationUrl'), spec.get('state'),
                                       spec.get('callbackUrl'), spec.get('clientCredsInHeaders'))


class OAuth2Authenticator(BaseAuthenticatorABC):
    spec_class = OAuth2AuthenticatorSpec

    def __init__(self, execution_spec: dict):
        super().__init__(execution_spec)
        self.debug_data = []

    def execute(self) -> AuthenticationResult:
        wrapper = RequestWrapper()
        requests_session = wrapper.session

        authorization_code = None
        try:
            if self.execution_spec.grant_type == 'authorization_code':
                authorization_code = self.call_authorization_url(requests_session)

            token = self.call_token_url(requests_session, authorization_code)

            return AuthenticationResult(
                AuthenticationStatus.SUCCESS,
                AuthenticationPayload(
                    headers={'Authorization': f'Bearer {token}'}
                ),
                wrapper.to_har(),
                self.debug_data
            )
        except:
            return AuthenticationResult(
                AuthenticationStatus.FAIL,
                AuthenticationPayload(
                    headers=None
                ),
                wrapper.to_har(),
                self.debug_data
            )

    def call_authorization_url(self, requests_session):
        try:
            resp = requests_session.request(
                method='POST',
                url=self.execution_spec.authorization_url,
                data={**self.get_auth_request_body(), 'response_type': 'code'},
                json=None,
                headers=self.get_auth_request_headers(),
                allow_redirects=False
            )
            resp.raise_for_status()
            redirect_location = resp.headers.get('location')
            if redirect_location is None:
                self.debug_data += ['No `location` header in authorization code response']
                raise BadAuthorizationCodeResponse()
            parsed_location = urlparse(redirect_location)
            parsed_location_query = parse_qs(parsed_location.query)

            authorization_code = parsed_location_query.get('code')
            if authorization_code is None:
                self.debug_data += ['No authorization code found in authorization code response']
                raise BadAuthorizationCodeResponse()
            return authorization_code

        except Exception as e:
            self.debug_data += ["Authorization code request failed", str(e)]
            raise e

    def call_token_url(self, requests_session, authorization_code):
        try:
            resp = requests_session.request(
                method='POST',
                url=self.execution_spec.token_url,
                data=self.get_auth_request_body(authorization_code),
                json=None,
                headers=self.get_auth_request_headers()
            )
            resp.raise_for_status()
            token_response = resp.json()
            if token_response.get('token_type', 'bearer').lower() != 'bearer':
                self.debug_data += [f'Unsupported token type {token_response.get("token_type")}']
                raise UnsupportedTokenTypeException()

            return self.extract_token_from_oauth_response(token_response)
        except Exception as e:
            self.debug_data += ["Token request failed", str(e)]
            raise e

    def get_auth_request_body(self, authorization_code=None):
        return get_without_none_values({
            'grant_type': self.execution_spec.grant_type,
            'client_id': self.execution_spec.client_id,
            'client_secret': self.execution_spec.client_secret,
            'username': self.execution_spec.username,
            'password': self.execution_spec.password,
            'scope': self.execution_spec.scope,
            'redirect_uri': self.execution_spec.callback_url,
            'state': self.execution_spec.state,
            'code': authorization_code
        })

    def get_auth_request_headers(self):
        request_headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        if self.execution_spec.client_creds_in_headers:
            request_headers['Authorization'] = 'Basic ' + base64.b64encode(f'{self.execution_spec.client_id}:{self.execution_spec.client_secret}'.encode()).decode('utf-8')
        return request_headers

    @staticmethod
    def extract_token_from_oauth_response(response_json):
        token = response_json.get('access_token', response_json.get('accessToken', response_json.get('token')))  # not everyone follows spec perfectly sadly
        if token is None:
            raise ValueError('token not found')
        return token


class UnsupportedTokenTypeException(Exception):
    pass


class BadAuthorizationCodeResponse(Exception):
    pass
