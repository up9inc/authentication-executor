from abc import ABC, abstractmethod
from enum import Enum

# TODO class
from typing import Dict, List, Optional


class AuthenticationStatus(Enum):
    FAIL = "FAIL"
    SUCCESS = "SUCCESS"


class AuthenticationPayload:
    def __init__(self, headers: Optional[Dict[str, str]], legacy_json=None):
        self.headers = headers
        self.legacy_json = legacy_json

    def to_dict(self):
        return {
            "headers": self.headers
        }


class AuthenticationResult:
    def __init__(self, status: AuthenticationStatus, payload: AuthenticationPayload, har_data: dict,
                 debug_data: List[str]):
        self.status = status
        self.payload = payload
        self.har_data = har_data
        self.debug_data = debug_data


class AuthenticationResultPostProcess:
    def __init__(self, result: AuthenticationResult, har_filename, config):
        self.result = result
        self.config = config
        self.har_filename = har_filename

    def to_dict(self):
        result_dict = {
            "payload": self.result.payload,
            # Currently supporting only headers
            "debugData": self.result.debug_data,
            "config": self.config,  # TODO serialize
            "status": self.result.status.value
        }

        if self.har_filename:
            result_dict["harFilename"] = self.har_filename

        return result_dict


class AuthSpecABC(ABC):
    @staticmethod
    @abstractmethod
    def from_dict(spec: dict):
        pass


class BaseAuthenticatorABC(ABC):
    spec_class: AuthSpecABC

    def __init__(self, execution_spec: dict):
        self.execution_spec = self.spec_class.from_dict(execution_spec)

    @abstractmethod
    def execute(self) -> AuthenticationResult:
        pass
