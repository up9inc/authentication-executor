import json
import os

from authentication_executor.authenticators.base_authenticator import AuthenticationPayload, AuthenticationResult, \
    AuthenticationStatus, AuthSpecABC, BaseAuthenticatorABC
from authentication_executor.util.request_wrapper import RequestWrapper


class AuthHelperAuthSpec(AuthSpecABC):
    @staticmethod
    def from_dict(spec: dict):
        return AuthHelperAuthSpec(spec)

    def __init__(self, spec):
        self.spec = spec


class AuthHelperAuthenticator(BaseAuthenticatorABC):
    spec_class = AuthHelperAuthSpec

    def execute(self) -> AuthenticationResult:
        wrapper = RequestWrapper()
        requests_session = wrapper.session
        auth_helper_server = os.environ.get('AUTH_HELPER_SERVER')

        if auth_helper_server is None:
            raise Exception("NO AUTH HELPER SERVER")

        status = AuthenticationStatus.SUCCESS
        auth_helper_response = None
        legacy_json = None
        debug_data = None

        try:
            resp = requests_session.post(f'http://{auth_helper_server}:3000', json=self.execution_spec.spec)
            auth_helper_response = resp.json()
            resp.raise_for_status()
        except BaseException as e:
            status = AuthenticationStatus.FAIL
        finally:
            requests_session.close()

        if auth_helper_response:
            debug_data = auth_helper_response["debugData"]
            debug_data.append(json.dumps(auth_helper_response["resultInfo"], indent=3))
            legacy_json = AuthHelperAuthenticator._convert_to_executor_format(auth_helper_response)

        return AuthenticationResult(
            status,
            AuthenticationPayload(headers=None, legacy_json=legacy_json),
            wrapper.to_har(),
            debug_data
        )

    @staticmethod
    def _convert_to_executor_format(auth_helper_dict):
        eps = auth_helper_dict["endpoints"]

        payloads = {
            "generated_payload_global": {
                "headers": auth_helper_dict["headers"]
            }
        }

        assignments = {
            "payloadId": "generated_payload_global"
        }

        for ep in eps:
            if ep["headers"] and len(ep["headers"]) > 0:
                payload_id = False
                for existing_payload_id, payload_val in payloads.items():
                    if payload_val["headers"] == ep["headers"]:
                        payload_id = existing_payload_id
                        break

                if not payload_id:
                    payload_id = f"generated_payload_{len(payloads)}"
                    payloads[payload_id] = {
                        "headers": ep["headers"]
                    }

                assignments.setdefault("services", {}).setdefault(ep["target"], {"endpoints": []})["endpoints"].append({
                    "method": ep["method"],
                    "path": ep["path"],
                    "payloadId": payload_id
                })

        return {
            "assignments": assignments,
            "entityPayloads": payloads,
            "cookies": auth_helper_dict["cookies"]
        }
