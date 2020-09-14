from abc import ABC, abstractmethod
from collections import namedtuple
from enum import Enum

# TODO class
from typing import Dict, List


class AuthenticationStatus(Enum):
    FAIL = "FAIL"
    SUCCESS = "SUCCESS"


class AuthenticationPayload:
    def __init__(self, headers: Dict[str, str]):
        self.headers = headers


class AuthenticationResult:
    def __init__(self, status: AuthenticationStatus, payload: AuthenticationPayload, har_data: dict,
                 debug_data: List[str]):
        self.status = status
        self.payload = payload
        self.har_data = har_data
        self.debug_data = debug_data


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
