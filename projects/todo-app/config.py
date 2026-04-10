"""Application configuration."""
import os
import warnings

# JWT secret key management
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
if SECRET_KEY == "dev-secret-key-change-in-production":
    warnings.warn(
        "SECRET_KEY is using default insecure value. Set SECRET_KEY environment variable in production.",
        RuntimeWarning,
        stacklevel=2,
    )

ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]
