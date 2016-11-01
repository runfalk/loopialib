from collections import namedtuple

__all__ = [
    "DnsRecord",
]

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
    def __new__(cls, type, ttl=None, priority=None, data=None, id=None):
        _validate_record_type(type)

        if ttl is None:
            ttl = 3600
        _validate_int("ttl", ttl)

        if priority is None:
            priority = 0
        _validate_int("priority", priority)

        if data is None:
            data = ""

        if id is None:
            id = 0
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


