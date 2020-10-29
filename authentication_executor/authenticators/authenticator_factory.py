from authentication_executor.authenticators.base_authenticator import BaseAuthenticatorABC
from .auth_helper_authenticator import AuthHelperAuthenticator
from .basic_auth_authenticator import BasicAuthAuthenticator
from .custom_code_authenticator import CustomCodeAuthenticator
from .headers_authenticator import HeadersAuthenticator
from .request_authenticator import RequestAuthenticator


class InvalidAuthenticator(Exception):
    pass


class AuthenticatorFactory:
    @staticmethod
    def create(config) -> BaseAuthenticatorABC:
        authenticator_type = config["type"]
        spec = config["spec"]
        if authenticator_type == 'customCode':
            return CustomCodeAuthenticator(spec)
        elif authenticator_type == 'tokenRequest':
            return RequestAuthenticator(spec)
        elif authenticator_type == 'authHelper':
            return AuthHelperAuthenticator(spec)
        elif authenticator_type == 'basicAuth':
            return BasicAuthAuthenticator(spec)
        elif authenticator_type == 'headers':
            return HeadersAuthenticator(spec)
        else:
            raise InvalidAuthenticator()


"""

A test run runs multiple payloads:
    id1: customCode1
    id2: customCode2

Some part needs to coordinate these and report

"""

# TODO migrate custom code to a new format, for now use _default_
