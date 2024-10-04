import os
# from datetime import timedelta
from dotenv import load_dotenv
from pydantic import BaseSettings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
load_dotenv(os.path.join(BASE_DIR, '.env'))


class Settings(BaseSettings):
    PROJECT_NAME = os.getenv('PROJECT_NAME', 'WINDY_COFFEE')
    SECRET_KEY = os.getenv('SECRET_KEY', '')
    X_API_KEY: str = "MIGeMA0GCSqGSIb3DQEBAQUAA4GMADCBiAKBgHdAa5TlL50FzyXvYkjbOWB77vZEOufX+URaegZEsxnwYW/gfDUfIdlEtefxOp7MczFPUcqcyFQNgCehOCqsHTrKA9KHsM/WbBjgAC9r+3ecBGu+IXgKk5YYD2AD9uIDgpgkS7en0jU+cdoeBKaLH5Tg+Bfo74xAOlz2LWxUJzILAgMBAAE="
    X_EMAIL_API_KEY: str = "frjQhnjZM3KroSO9ZPa3AuHH4wwQGEF0ZBBRifLYLQ3YJCGL2ju7tncj4pBp9qVdJqeqJTTacCwWJKBYefljBE2BRyTzW9BUIMWuTYPGryxIBKBnDboWy7Rxrmwq95qlux008Pv4ncb3gsdnV8Mvcmryaf4FCYlJtfxn4N35x0EXWzDQJcNHSCHoup1CzAForajnDRrXQ5iq2O75BXM5yrZXMKlDDJfrq6Pqqp89EdEbH149RlTfjsXpBrW90Onu"
    JWT_REFREwdc_SECRET_KEY: str = "MOWB77vZEOufX+URaegZEsxnwYW/gfDUfIdlEtefxOp7MczFPUcqcyFQNgCehOCqsHTrKA9KHsM/WbBjgAC9r+3ecBGu+ZEsxnwYW/gfDUfIdlEtefxOp7MczFPUcqcykS7en0jU+cdoeBKaLH5FQNgCehO="
    AWS_SERVER_PUBLIC_KEY: str = "AKIA3S75Q7FFFKPVM3FR"
    AWS_SERVER_SECRET_KEY: str = "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"
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 1  # Token expired after 1 days
    REFREwdc_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 90  # Token expired after 90 days
    API_PREFIX = '/api/v1'
    BACKEND_CORS_ORIGINS = ['*']
    DATABASE_URL = os.getenv('SQL_DATABASE_URL', '')
    # DEFAULT_EXPIRY: int = timedelta(hours=10)
    SECURITY_ALGORITHM = 'HS256'
    EMAIL_SERVICE = ''
    LOGGING_CONFIG_FILE = os.path.join(BASE_DIR, 'logging.ini')
    AUTHJWT_SECRET_KEY: str = os.getenv('SECRET_KEY', '')
    REDIS_URL: str = os.getenv('REDIS_URL', '')
    REDIS_MAX_CONNECTION: int = os.getenv('REDIS_MAX_CONNECTION', 20)
    EMAIL_BLACKLIST = ['nxtho0109@gmail.com', ]


settings = Settings()  
