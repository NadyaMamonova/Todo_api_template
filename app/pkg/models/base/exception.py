"""Base exception for API."""

from typing import Optional, Union, Dict, Any

from fastapi import HTTPException
from starlette import status

from app.pkg.models.types.strings import NotEmptyStr

__all__ = ["BaseAPIException", "BaseAppException"]


class BaseAppException(Exception):
    """Base application exception (not HTTP-related)."""
    message: Optional[Union[NotEmptyStr, str]] = "Base Application Exception"
    template: Optional[str] = None
    template_context: Optional[Dict[str, Any]] = None

    def __init__(
        self,
        message: Optional[Union[NotEmptyStr, str, Exception]] = None,
        template_context: Optional[Dict[str, Any]] = None,
    ):
        if message is not None:
            self.message = message

        if isinstance(message, Exception):
            self.message = str(message)

        if template_context:
            self.template_context = template_context
            if self.template:
                self.message = self.template.format(**self.template_context)

        super().__init__(self.message)


class BaseAPIException(HTTPException):
    """Base internal API Exception.

    Attributes:
        message:
            Message of exception.
        status_code:
            Status code of exception.
        template:
            String template for message formatting.
        template_context:
            Context for template formatting.

    Examples:
        Before using this class, you must create your own exception class.
        And inherit from this class.::

            >>> from app.pkg.models.base.exception import BaseAPIException
            >>> from starlette import status
            >>> class MyException(BaseAPIException):
            ...     message = "My exception"
            ...     status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            ...     template = "Error with {item} when processing {action}"

        After that, you can use it in your code in some function run under fastapi::

            >>> async def my_func():
            ...     raise MyException(template_context={"item": "user", "action": "registration"})
    """

    message: Optional[Union[NotEmptyStr, str]] = "Base API Exception"
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    template: Optional[str] = None
    template_context: Optional[Dict[str, Any]] = None

    def __init__(
        self,
        message: Optional[Union[NotEmptyStr, str, Exception]] = None,
        template_context: Optional[Dict[str, Any]] = None,
    ):
        """Init BaseAPIException.

        Args:
            message:
                Message of exception by default is "Base API Exception".
            template_context:
                Context for template formatting.
        """
        if message is not None:
            self.message = message

        if isinstance(message, Exception):
            self.message = str(message)

        if template_context:
            self.template_context = template_context
            if self.template:
                self.message = self.template.format(**self.template_context)

        super().__init__(status_code=self.status_code, detail=self.message)

    @classmethod
    def generate_openapi(cls):
        return {
            cls.status_code: {
                "description": cls.message,
                "content": {
                    "application/json": {
                        "example": {
                            "message": cls.message,
                        },
                    },
                },
            },
        }
