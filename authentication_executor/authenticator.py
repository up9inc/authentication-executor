import json
from abc import ABC, abstractmethod
from enum import Enum
from uuid import uuid4

from authentication_executor.authenticators.authenticator_factory import AuthenticatorFactory
from authentication_executor.authenticators.base_authenticator import AuthenticationResultPostProcess, \
    AuthenticationStatus


class AuthExecutionStatus(Enum):
    FAIL = "FAIL"
    SUCCESS = "SUCCESS"


class AuthExecutionResult:
    def __init__(self, _id, result_json):
        self.id = _id
        self.json = result_json


class BucketUploaderABC(ABC):
    @abstractmethod
    def upload(self, data, content_type, signed_url):
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
    def __init__(self, bucket_uploader: BucketUploaderABC, url_signer: URLSignerABC, api_client: ApiClientABC, logger):
        self.api_client = api_client
        self.url_signer = url_signer
        self.bucket_uploader = bucket_uploader
        self.execution_id = self.api_client.create_execution_id()
        self.logger = logger

    # TODO perhaps this should return a class with JSON serialization
    def _process_config(self, config_id, config):
        extra = {
            "configId": config_id
        }

        executor = AuthenticatorFactory.create(config)
        self.logger.info("Executing authentication config", extra=extra)
        result = executor.execute()

        self.logger.info("Done executing", extra={
            **extra,
            "status": result.status.value
        })
        har_filename = None
        if result.har_data:
            har_filename = f"{config_id}_{str(uuid4())[:6]}.har"
            signed_url = self.url_signer.get_signed_url(self.execution_id, har_filename)
            self.logger.info("Uploading HAR")
            self.bucket_uploader.upload(json.dumps(result.har_data).encode('utf-8'), "text/plain", signed_url)
            self.logger.info("Done uploading HAR")

        return AuthenticationResultPostProcess(
            result,
            har_filename,
            config
        )

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
        self.logger.info("Starting authentication execution", extra={
            "executionId": self.execution_id
        })

        results = {config_id: self._process_config(config_id, config) for config_id, config in auth_configs.items() if self._should_execute(config_id, assignments)}

        did_any_fail = any(post_process_result.result.status != AuthenticationStatus.SUCCESS for post_process_result in results.values())

        self.api_client.persist_results(self.execution_id, {
            "executions": {k: v.to_dict() for k, v in results.items()},
            "status": AuthExecutionStatus.FAIL.value if did_any_fail else AuthExecutionStatus.SUCCESS.value
        })

        if did_any_fail:
            raise Exception("Authentication Execution Failed!")

        return AuthExecutionResult(
            self.execution_id,
            Authenticator._to_result_dict(assignments, results)
        )

    @staticmethod
    def _to_result_dict(assignments, results):
        legacy_result = next(filter(lambda post_process_result: post_process_result.result.payload is not None and post_process_result.result.payload.legacy_json is not None, results.values()), None)

        if legacy_result:
            return legacy_result.result.payload.legacy_json

        return {
            'entityPayloads': {config_id: post_process_result.result.payload.to_dict() for config_id, post_process_result in results.items()},
            **assignments
        }

    def _should_execute(self, config_id, assignments):
        if assignments.get('payloadId') == config_id:
            return True

        for svc_target_name, svc_config in assignments.get('services', {}).items():
            if svc_config.get('payloadId') == config_id:
                return True
            for ep_config in svc_config.get('endpoints', []):
                if ep_config['payloadId'] == config_id:
                    return True

        return False
