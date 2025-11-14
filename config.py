"""
Configuration module for MCP server.
Handles environment variables and application settings.
"""

import os
from typing import Optional


class Config:
    """Application configuration."""

    # Server settings
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', '8080'))  # Cloud Run uses PORT env variable
    DEBUG: bool = os.getenv('DEBUG', 'false').lower() == 'true'

    # Database settings
    DB_PATH: str = os.getenv('DB_PATH', os.path.join(os.getcwd(), 'data', 'customers.db'))

    # MCP Protocol settings
    PROTOCOL_VERSION: str = '2024-11-05'
    SERVER_NAME: str = 'customer-management-server'
    SERVER_VERSION: str = '1.0.0'

    # Logging settings
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')

    @classmethod
    def get_db_path(cls) -> str:
        """Get the database path, ensuring it's absolute."""
        if os.path.isabs(cls.DB_PATH):
            return cls.DB_PATH
        return os.path.abspath(cls.DB_PATH)

    @classmethod
    def validate(cls):
        """Validate configuration settings."""
        if cls.PORT < 1 or cls.PORT > 65535:
            raise ValueError(f"Invalid port number: {cls.PORT}")

        if cls.LOG_LEVEL not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            raise ValueError(f"Invalid log level: {cls.LOG_LEVEL}")
