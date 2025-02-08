import secrets
# class Config:
#     SECRET_KEY = 'no_matter_what'
#     MYSQL_HOST = 'localhost'
#     MYSQL_USER = 'root'
#     MYSQL_PASSWORD = '123456'
#     MYSQL_DB = 'sky31Employees'
#     MYSQL_CHARSET='utf8mb4'
#     MYSQL_AUTOCOMMIT=True
class Config:
    SECRET_KEY = secrets.token_urlsafe(64)
