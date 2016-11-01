from .exceptions import LoopiaError
from .types import DnsRecord, _validate_int

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

    def get_subdomains(self, domain):
        return self._call("getSubdomains", domain)

    def remove_subdomain(self, domain, subdomain=None):
        if subdomain is None:
            subdomain = "@"

        return self._call("removeSubdomain", domain, subdomain)

    def add_zone_record(self, record, domain, subdomain=None):
        if subdomain is None:
            subdomain = "@"

        if record.id != 0:
            raise ValueError("Record must not have an ID")

        self._call("addZoneRecord", domain, subdomain, record.to_dict())

    def get_zone_records(self, domain, subdomain=None):
        if subdomain is None:
            subdomain = "@"

        return [
            DnsRecord.from_dict(record)
            for record in self._call("getZoneRecords", domain, subdomain)
        ]

    def update_zone_record(self, record, domain, subdomain=None):
        if subdomain is None:
            subdomain = "@"

        self._call("updateZoneRecord", domain, subdomain, record.to_dict())

    def remove_zone_record(self, id, domain, subdomain=None):
        """
        Remove the zone record with the given ID that belongs to the given
        domain and sub domain. If no sub domain is given the wildcard sub-domain
        is assumed.
        """

        if subdomain is None:
            subdomain = "@"

        _validate_int("id", id)

        self._call("removeZoneRecord", domain, subdomain, id)


class LoopiaTest(Loopia):
    base_url = "https://test-api.loopia.se/RPCSERV"
