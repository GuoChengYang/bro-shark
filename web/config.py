# config.py


import os


class BaseConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
    DEBUG = os.environ.get('DEBUG') or True
    DB_NAME = os.environ.get('DB_NAME') or 'postgres'
    DB_USER = os.environ.get('DB_USER') or 'postgres'
    DB_PASS = os.environ.get('DB_PASS') or 'postgres'
    DB_SERVICE = os.environ.get('DB_SERVICE') or 'localhost'
    DB_PORT = os.environ.get('DB_PORT') or 5432
    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
        DB_USER, DB_PASS, DB_SERVICE, DB_PORT, DB_NAME
    )
    # SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}/{2}'.format(
    #     DB_SERVICE, DB_PORT, DB_NAME
    # )

# class BaseConfig(object):
#     SECRET_KEY = 'hi'
#     DEBUG = True
#     DB_NAME = 'postgres'
#     DB_SERVICE = 'localhost'
#     DB_PORT = 5432
#     SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}/{2}'.format(
#         DB_SERVICE, DB_PORT, DB_NAME
#     )
