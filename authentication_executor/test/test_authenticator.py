import unittest

from authentication_executor.authenticator import Authenticator, ApiClientABC, URLSignerABC
from authentication_executor.test.test_authentication import configs_1
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
    ApiClientMock()
)


class AuthenticatorTests(unittest.TestCase):
    def test_aggregate_results(self):
        execute = authenticator.execute(configs_1, {"payloadId": "XXX_ZZZ"})
        self.assertEqual(execute.json['entityPayloads']['XXX_ZZZ']['headers']['Auth'], '1')


if __name__ == '__main__':
    unittest.main()
