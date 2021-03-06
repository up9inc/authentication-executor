import datetime
import requests
from urllib.parse import parse_qs, urlparse


# TODO transform cookies
class RequestWrapper:
    def __init__(self):
        self._entries = []
        self.session = requests.Session()
        self.session.hooks['response'] = [self._produce_entry]

    def to_har(self):
        if len(self._entries) == 0:
            return None

        return {
            "log": {
                "version": "1.2",
                "creator": {"name": "up9 authenticator", "version": "0.1", "comment": ""},
                "entries": self._entries
            }
        }

    @staticmethod
    def _dict_to_array(headers):
        return [{"name": key, "value": str(val)} for key, val in headers.items()]

    @staticmethod
    def _transform_body(request):
        if request.body is None:
            return None

        return {
            "mimeType": request.headers.get('content-type', '?'),
            "text": str(request.body)
            # TODO missing params, body is interepreted as bytes
        }

    def _produce_entry(self, resp, *args, **kwargs):
        request = resp.request
        query = urlparse(request.url).query
        self._entries.append({
            "startedDateTime": (datetime.datetime.now() - resp.elapsed).astimezone().isoformat(),
            # TODO datetime.datetime.now() - resp.elapsed,	
            "time": 0,
            "request": {
                "method": request.method,
                "httpVersion": '',
                "cookies": [],  # TODO list(request.cookies),
                "headers": RequestWrapper._dict_to_array(request.headers),
                "queryString": RequestWrapper._dict_to_array(parse_qs(query)) if query else [],
                "headersSize": -1,  # TODO len(json.dumps(request.headers)),
                "bodySize": -1,     # TODO len(json.dumps(request.body)) if request.body else 0,
                "postData": RequestWrapper._transform_body(request),
                "url": request.url
            },
            "response": {
                "status": resp.status_code,
                "statusText": resp.reason,
                "httpVersion": '',
                "cookies": [],  # TODO list(resp.cookies),
                "headers": RequestWrapper._dict_to_array(resp.headers),
                "content": {
                    "size": resp.headers.get('content-length') or len(resp.text),
                    "compression": 0,
                    "mimeType": resp.headers.get('content-type', '?'),
                    "text": resp.text[:10000]
                },
                "bodySize": len(resp.text),
                "headersSize": -1,  # TODO,
                "redirectURL": resp.headers.get('location') or ""
            },
            "cache": {},
            "timings": {
                "send": -1,
                "receive": resp.elapsed.total_seconds() * 1000,
                "wait": -1
            }
        })
