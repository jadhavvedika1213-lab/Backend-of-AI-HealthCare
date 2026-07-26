from fastapi import status

class BaseHealthcareException(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class UserNotFoundException(BaseHealthcareException):
    def __init__(self, message: str = "User not found"):
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)

class InvalidCredentialsException(BaseHealthcareException):
    def __init__(self, message: str = "Incorrect email or password"):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)

class PermissionDeniedException(BaseHealthcareException):
    def __init__(self, message: str = "Operation not permitted"):
        super().__init__(message, status_code=status.HTTP_403_FORBIDDEN)

class ResourceNotFoundException(BaseHealthcareException):
    def __init__(self, message: str = "Requested resource not found"):
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)

class OCRProcessingException(BaseHealthcareException):
    def __init__(self, message: str = "Failed to extract text from document"):
        super().__init__(message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

class AIServiceException(BaseHealthcareException):
    def __init__(self, message: str = "AI generation failed"):
        super().__init__(message, status_code=status.HTTP_502_BAD_GATEWAY)

class EmailSendingException(BaseHealthcareException):
    def __init__(self, message: str = "Failed to send email"):
        super().__init__(message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
