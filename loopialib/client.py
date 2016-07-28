from .exceptions import LoopiaError
from .types import DnsRecord

try:
    # Python 2
    from xmlrpclib import ServerProxy
except ImportError:
    # Python 3
    from xmlrpc.client import ServerProxy

try:
    # Python 2
    string_types = basestring
except NameError:
    # Python 3
    string_types = (str, bytes)

class Loopia(object):
    base_url = "https://api.loopia.se/RPCSERV"
    encoding = "utf-8"

    def __init__(self, user, password):
        self.user = user
        self.password = password
        self._client = ServerProxy(self.base_url, encoding=self.encoding)

    def _call(self, method, *args):
        response = getattr(self._client, method)(self.user, self.password, *args)
        if len(response) == 1 and isinstance(response[0], string_types):
            if response[0] == "OK":
                return True
            raise LoopiaError.from_code(response[0], response)
        return response

    def get_zone_records(self, domain, sub_domain=None):
        if sub_domain is None:
            sub_domain = "@"

        return [
            DnsRecord.from_dict(record)
            for record in self._call("getZoneRecords", domain, sub_domain)
        ]

    def update_zone_record(self, record, domain, sub_domain=None):
        if sub_domain is None:
            sub_domain = "@"

        self._call("updateZoneRecord", domain, sub_domain, record.to_dict())


class LoopiaTest(Loopia):
    base_url = "https://test-api.loopia.se/RPCSERV"
