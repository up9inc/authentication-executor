import json
import logging
import os
import unittest

from authentication_executor import BucketUploaderABC
from authentication_executor.authenticator import ApiClientABC, Authenticator, URLSignerABC
from authentication_executor.test.data import configs


class BucketUploaderMock(BucketUploaderABC):
    def upload(self, data, filename, signed_url) -> str:
        return '/stub/file.har'


class ApiClientMock(ApiClientABC):
    def create_execution_id(self):
        return 'exeuctionId1'

    def persist_results(self, execution_id, _json):
        json.dumps(_json)
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

    def test_should_execute(self):
        assignments = {
            "payloadId": "global1", "services": {
                "svc2": {
                    "payloadId": "svc2p"
                },
                "svc3": {
                    "endpoints": [{
                        "payloadId": "ep1p"
                    }]
                }
            }}
        should_execute = authenticator._should_execute("global1", assignments)
        self.assertTrue(should_execute)
        should_execute = authenticator._should_execute("svc2p", assignments)
        self.assertTrue(should_execute)
        should_execute = authenticator._should_execute("ep1p", assignments)
        self.assertTrue(should_execute)
        should_execute = authenticator._should_execute("nonExistent", assignments)
        self.assertFalse(should_execute)


if __name__ == '__main__':
    unittest.main()
