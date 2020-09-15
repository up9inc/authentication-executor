import json
from abc import ABC, abstractmethod
from enum import Enum
from uuid import uuid4

from testr.logger.logging_util import LoggerFactory

from authentication_executor.authenticators.base_authenticator import AuthenticationStatus

logger = LoggerFactory.get_logger(__name__)

from authentication_executor.authenticators.authenticator_factory import AuthenticatorFactory


class AuthExecutionStatus(Enum):
    FAIL = "FAIL"
    SUCCESS = "SUCCESS"


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
    def __init__(self, bucket_uploader: BucketUploaderABC, url_signer: URLSignerABC, api_client: ApiClientABC):
        self.api_client = api_client
        self.url_signer = url_signer
        self.bucket_uploader = bucket_uploader
        self.execution_id = self.api_client.create_execution_id()

    # TODO perhaps this should return a class with JSON serialization
    def _process_config(self, config_id, config):
        extra = {
            "configId": config_id
        }

        executor = AuthenticatorFactory.create(config)
        logger.info("Executing authentication config", extra=extra)
        result = executor.execute()
        logger.info("Done executing", extra={
            **extra,
            "status": result.status.value
        })
        har_filename = f"{config_id}_{str(uuid4())[:6]}.har"
        signed_url = self.url_signer.get_signed_url(self.execution_id, har_filename)
        logger.info("Uploading HAR")
        self.bucket_uploader.upload(json.dumps(result.har_data).encode('utf-8'), "text/plain", signed_url)
        logger.info("Done uploading HAR")

        # TODO this is quite similar to the result itself, can we merge somehow
        return {
            "harFilename": har_filename,
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
        LoggerFactory.set_extra_global_context({
            "executionId": self.execution_id
        })

        logger.info("Starting authentication execution")

        results = {k: self._process_config(k, v) for k, v in auth_configs.items()}

        did_any_fail = any(result["status"] != AuthenticationStatus.SUCCESS.value for result in results.values())

        self.api_client.persist_results(self.execution_id, {
            "executions": results,
            "status": AuthExecutionStatus.FAIL.value if did_any_fail else AuthExecutionStatus.SUCCESS.value
        })

        if did_any_fail:
            raise Exception("Authentication Execution Failed!")

        LoggerFactory.set_extra_global_context({
            "executionId": None
        })

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
