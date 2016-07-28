from collections import namedtuple

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


__version__ = "0.1.0"


def _validate_int(name, value):
    if type(value) is not int:
        raise TypeError("Expected '{name}' to be 'int', got '{value}'".format(
            name=name,
            value=type(value).__name__))

    if value < 0:
        raise ValueError("'{name}' must not be less than 0".format(name=name))


_record_types = frozenset([
    "A", "AAAA", "CERT", "CNAME", "HINFO", "HIP", "IPSECKEY", "LOC",
    "MX", "NAPTR", "NS", "SRV", "SSHFP", "TXT"])


def _validate_record_type(type):
    if type not in _record_types:
        raise ValueError("Type '{type}' is not either of ({types})".format(
            type=type,
            types=", ".join(_record_types)))


_DnsRecord = namedtuple("_DnsRecord", ["type", "ttl", "priority", "data", "id"])
class DnsRecord(_DnsRecord):
    def __new__(cls, type, ttl, priority, data, id):
        _validate_record_type(type)
        _validate_int("ttl", ttl)
        _validate_int("priority", priority)
        _validate_int("id", id)

        return super(DnsRecord, cls).__new__(cls, type, ttl, priority, data, id)

    def _replace(self, **kwargs):
        if "type" in kwargs:
            _validate_record_type(kwargs["type"])

        for attr in ("ttl", "priority", "id"):
            if attr in kwargs:
                _validate_int(attr, kwargs[attr])

        return super(DnsRecord, self)._replace(**kwargs)

    replace = _replace

    def __repr__(self):
        return super(DnsRecord, self).__repr__().lstrip("_")

    @classmethod
    def from_dict(cls, record):
        return cls(
            type=record["type"],
            ttl=record["ttl"],
            priority=record["priority"],
            data=record["rdata"],
            id=record["record_id"])

    def to_dict(self):
        return {
            "type": self.type,
            "ttl": self.ttl,
            "priority": self.priority,
            "rdata": self.data,
            "record_id": self.id,
        }


class LoopiaError(Exception):
    errors = {
        "AUTH_ERROR": u"Wrong username or password",
        "DOMAIN_OCCUPIED": u"Domain is not available for registration",
        "RATE_LIMITED": u"Maximum number of reguests over time reached",
        "BAD_INDATA": u"Invalid parameters",
        "INSUFFICIENT_FUNDS": "Not enough funds to complete the task",
    }
    def __init__(self, message, code=None, response=None):
        super(LoopiaError, self).__init__(message)
        self.code = code
        self.response = response

    @classmethod
    def from_code(cls, code, response=None):
        message = cls.errors.get(code, "Unknown error '{code}'").format(
            code=code)

        return cls(message, code, response)


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
