import logging
import os
import unittest

from authentication_executor.authenticator import Authenticator, ApiClientABC, URLSignerABC
from authentication_executor.test.data import configs_1, configs
from authentication_executor import BucketUploaderABC


class BucketUploaderMock(BucketUploaderABC):
    def upload(self, data, filename, signed_url) -> str:
        return '/stub/file.har'


class ApiClientMock(ApiClientABC):
    def create_execution_id(self):
        return 'exeuctionId1'

    def persist_results(self, json, execution_id):
        return ''


class URLSignerMock(URLSignerABC):
    def get_signed_url(self, execution_id, filename):
        return "stubURL"


authenticator = Authenticator(
    BucketUploaderMock(),
    URLSignerMock(),
    ApiClientMock(),
    logging.getLogger("AuthExecutor")
)


class AuthenticatorTests(unittest.TestCase):
    def test_aggregate_results(self):
        os.environ['AUTH_HELPER_SERVER'] = "localhost:3001"
        configs.pop('AUTH_HELPER')
        execute = authenticator.execute(configs, {"payloadId": "XXX_ZZZ"})
        self.assertEqual(execute.json['entityPayloads']['XXX_ZZZ']['headers']['Auth'], '2')


if __name__ == '__main__':
    unittest.main()
