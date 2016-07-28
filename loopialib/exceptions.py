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
