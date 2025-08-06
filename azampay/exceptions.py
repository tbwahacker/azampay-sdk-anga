class AzamPayException(Exception):
    """Base exception for AzamPay SDK."""
    def __init__(self, message=None):
        super().__init__(message or "An error occurred in AzamPay SDK")


class AuthenticationError(AzamPayException):
    """Raised when authentication fails."""
    def __init__(self, message=None):
        super().__init__(message or "Authentication with AzamPay failed")


class CheckoutError(AzamPayException):
    """Raised when checkout fails."""
    def __init__(self, message=None):
        super().__init__(message or "Checkout process failed with AzamPay")


class EnvironmentError(AzamPayException):
    """Raised when required environment variables are missing."""
    def __init__(self, key=None):
        message = f"Missing required environment variable: {key} in .env file" if key else "Missing required environment variable  in .env file"
        super().__init__(message)
