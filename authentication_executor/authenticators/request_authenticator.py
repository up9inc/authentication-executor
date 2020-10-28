import re
from typing import Dict

from jsonpath_ng import parse

from authentication_executor.authenticators.base_authenticator import AuthenticationPayload, AuthenticationResult, \
    AuthenticationStatus, AuthSpecABC, \
    BaseAuthenticatorABC
from authentication_executor.util.request_wrapper import RequestWrapper


class RequestAuthenticatorSpec(AuthSpecABC):
    def __init__(self, request: Dict, payload: Dict):
        self.request = request
        self.payload = payload

    @staticmethod
    def from_dict(spec: dict):
        return RequestAuthenticatorSpec(spec["request"], spec["payload"])


class RequestAuthenticator(BaseAuthenticatorABC):
    spec_class = RequestAuthenticatorSpec

    def execute(self) -> AuthenticationResult:
        wrapper = RequestWrapper()
        requests_session = wrapper.session

        request_spec = self.execution_spec.request
        payload_spec = self.execution_spec.payload

        debug_data = []
        headers = None

        status = AuthenticationStatus.SUCCESS

        try:
            resp = requests_session.request(
                method=request_spec['method'],
                url=request_spec['url'],
                data=request_spec.get('body') if request_spec['type'] == "x-www-form-urlencoded" else None,
                json=request_spec.get('body') if request_spec['type'] == "json" else None,
                headers={item['key']: item['value'] for item in request_spec.get('headers', [])}
            )
            resp.raise_for_status()
        except Exception as e:
            debug_data.append("Request failed")
            debug_data.append(str(e))
            status = AuthenticationStatus.FAIL

        if status != AuthenticationStatus.FAIL:
            try:
                value_json_path_str = payload_spec['valueJsonPath']
                json_path_str = re.search("\$[^\s]*", value_json_path_str).group()
                json_path_expr = parse(json_path_str)
            except Exception as e:
                debug_data.append("Failed to parse json path")
                debug_data.append(str(e))
                status = AuthenticationStatus.FAIL

        if status != AuthenticationStatus.FAIL:
            try:
                token = json_path_expr.find(resp.json())[0].value
                header_value = value_json_path_str.replace(json_path_str, token)

                headers = {
                    payload_spec['header']: header_value
                }
            except Exception as e:
                debug_data.append("Failed to find value in response")
                debug_data.append(str(e))
                status = AuthenticationStatus.FAIL

        requests_session.close()
        print(debug_data)
        return AuthenticationResult(
            status,
            AuthenticationPayload(
                headers=headers
            ),
            wrapper.to_har(),
            debug_data
        )
