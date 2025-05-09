from app.pkg.models.base.exception import BaseAPIException
from starlette import status

class TaskNotFound(BaseAPIException):
    message = "Task not found"
    status_code = status.HTTP_404_NOT_FOUND

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

class TaskAlreadyExists(BaseAPIException):
    message = "Task already exists"
    status_code = status.HTTP_409_CONFLICT

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

class TaskAPIError(BaseAPIException):
    message = "Task API error"
    status_code = status.HTTP_400_BAD_REQUEST
    template = "Task error: {reason}"