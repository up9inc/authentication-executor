import json
from abc import ABC, abstractmethod
from uuid import uuid4

from authentication_executor.authenticators.authenticator_factory import AuthenticatorFactory
from authentication_executor.authenticators.base_authenticator import AuthenticationResult


class AuthExecutionResult:
    def __init__(self, _id, json):
        self.id = _id
        self.json = json


class SignedURLGeneratorABC(ABC):
    @abstractmethod
    def get_signed_url(self, *args, **kwargs):
        pass


class BucketUploaderABC(ABC):
    @abstractmethod
    def upload(self, data, content_type, signed_url) -> str:
        pass


class ApiClientABC(ABC):
    @abstractmethod
    def create_execution_id(self) -> str:
        pass

    @abstractmethod
    def persist_results(self, execution_id, json):
        pass


class URLSignerABC(ABC):
    @abstractmethod
    def get_signed_url(self, execution_id, filename):
        pass


class Authenticator:
    def __init__(self, bucket_uploader: BucketUploaderABC, url_signer: URLSignerABC, api_client: ApiClientABC):
        # self.api = api
        self.api_client = api_client
        self.url_signer = url_signer
        self.bucket_uploader = bucket_uploader
        self.execution_id = self.api_client.create_execution_id()
        # def get_signed_url(filename):
        #     return api.get_signed_url(self.execution_id, filename)

    # TODO merge with execute()
    @staticmethod
    def verify_config(config) -> AuthenticationResult:
        executor = AuthenticatorFactory.create(config)
        return executor.execute()

    # TODO perhaps this should return a class with JSON serialization
    def _process_config(self, config_id, config):
        executor = AuthenticatorFactory.create(config)
        result = executor.execute()
        signed_url = self.url_signer.get_signed_url(self.execution_id, f"{config_id}_{str(uuid4())}.har")
        har_path = self.bucket_uploader.upload(json.dumps(result.har_data).encode('utf-8'), "text/plain", signed_url)

        # TODO this is quite similar to the result itself, can we merge somehow
        return {
            "harPath": har_path,
            "payload": {"headers": result.payload.headers} if result.payload else None,
            # Currently supporting only headers
            "debugData": result.debug_data,
            "config": config,  # TODO serialize
            "status": result.status.value,
        }

    def execute(self, auth_configs, assignments) -> AuthExecutionResult:
        """
        :param auth_configs: {
            "ID_0": {
                type: "customCode",
                spec: {
                    customCode: "XXX==="
                }
            },
            "ID_2" : {
                type: "customCode",
                spec: {
                    customCode: "ZZZ==="
                }
            }
        }
        :param assignments: {
            payloadId: "ID_0",
            services: {
                "TARGET_SVC_1": {
                    payloadId: "ID_2"
                }
            }
        }
        :return: Aggregated result for env var
        """

        results = {k: self._process_config(k, v) for k, v in
                   auth_configs.items()}  # list(map(self._process_config, auth_configs.items()))

        did_any_fail = any(result["status"] != "SUCCESS" for result in results.values())

        self.api_client.persist_results(self.execution_id, {
            "executions": results,
            "status": "FAILED" if did_any_fail else "SUCCESS"  # TODO enum and improve
        })

        if did_any_fail:
            raise Exception("Authentication Execution Failed!")

        return AuthExecutionResult(
            self.execution_id,
            Authenticator._to_result_dict(assignments, results)
        )

    @staticmethod
    def _to_result_dict(assignments, results):
        return {
            'entityPayloads': {config_id: config['payload'] for config_id, config in results.items()},
            **assignments
        }


"""

A test run runs multiple payloads:
    id1: customCode1
    id2: customCode2

Some part needs to coordinate these and report



1. Persist config/assignment object differently from FE->TRCC *
2. Produce HAR from requests *
3. Upload HARs *
4. Persist auth result to TRCC *
5. Persist test run with auth result to TRCC
...

* RCA -> display results + HAR in test run
* Support verify flow in test run
* FE -> add verify button + read results
* Test auth helper still works
* Custom code migration script
* Thread for uploading HARs
* Consider separating the authenticator service / job
* Release new test runner etc
* Handle test runner duplication thing for ECS
* Improve HAR conversion
* tests for HAR conversion/extract to joint library?
* Logging
* Handle lingering status
* Test impersonation in test run + verify

"""
