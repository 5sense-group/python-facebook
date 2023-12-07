from attr import attrs, attrib, asdict
from typing import Optional

__all__ = [
    "PyFacebookError", "ErrorCode", "ErrorMessage",
    "PyFacebookException", "PyFacebookDeprecationWaring"
]


class PyFacebookError(Exception):
    """ Base class for PyFacebook errors"""

    @property
    def message(self):
        """ return the error's first arg """
        return self.args[0]  # pragma: no cover


class ErrorCode:
    HTTP_ERROR = 10000
    MISSING_PARAMS = 10001
    INVALID_PARAMS = 10002
    NOT_SUPPORT_METHOD = 10010


@attrs
class ErrorMessage(object):
    code = attrib(default=None, type=Optional[str])
    message = attrib(default=None, type=Optional[str])
    error_type = attrib(default="PyFacebookException", type=Optional[str])
    error_subcode = attrib(default="None", type=Optional[str])
    error_user_title = attrib(default="None", type=Optional[str])
    error_user_msg = attrib(default="None", type=Optional[str])


class PyFacebookException(Exception):
    """
    Library exception class.

    Show internal error and api response error.
    """

    def __init__(self, data):
        self.data = None
        self.message = None
        self.type = None
        self.code = None
        self.error_subcode = None
        self.error_user_title = None
        self.error_user_msg = None
        self.fbtrace_id = None
        self.error_type = None
        self.initial(data)

    def initial(self, data):
        """
        Args:
             data (dict,ErrorMessage):
                1. Internal error data is an instance of ErrorMessage.
                2. Api response error is dict.
                   Refer: https://developers.facebook.com/docs/graph-api/using-graph-api/error-handling
        """
        if isinstance(data, ErrorMessage):
            self.message = data.message
            self.error_type = data.error_type
            self.type = data.error_type
            self.code = data.code
            self.error_subcode = data.error_subcode
            self.error_user_title = data.error_user_title
            self.error_user_msg = data.error_user_msg
            self.data = asdict(data)
        elif isinstance(data, dict):
            self.error_type = "FacebookException"
            self.message = data.get("message")
            self.type = data.get("type")
            self.code = data.get("code")
            self.error_subcode = data.get("error_subcode")
            self.error_user_title = data.get("error_user_title")
            self.error_user_msg = data.get("error_user_msg")
            self.fbtrace_id = data.get("fbtrace_id")
            self.data = {"error": data}

    def __repr__(self):
        return (
            "{0}(code={1},type={2},message={3},error_subcode={4},error_user_title={5},error_user_msg={6})".format(
                self.error_type, self.code, self.type, self.message, self.error_subcode, self.error_user_title, self.error_user_msg
            )
        )

    def __str__(self):
        return self.__repr__()


class PyFacebookDeprecationWaring(DeprecationWarning):
    pass
