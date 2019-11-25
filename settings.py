import secrets
import json

db = ''
with open('database.json', 'r') as database:
    data = json.load(database)
    db = (
        data['host'],
        data['port'],
        data['user'],
        data['password'],
        data['database'])


class Settings:
    SECRET_KEY = secrets.token_hex(32)
    SECURITY_PASSWORD_SALT = secrets.token_hex(4)
    JWT_SECRET_KEY = 'secret-key'

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = '070d856@gmail.com'
    MAIL_PASSWORD = 'f1f2f3f4f5'
    MAIL_DEFAULT_SENDER = 'LSD'

    # f'postgresql://{db[2]}:{db[3]}@{db[0]}:{db[1]}/{db[4]}'
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = True
