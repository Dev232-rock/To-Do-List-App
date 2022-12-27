
class Config:
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    # secret key for test created by secret lib ib python
    SECRET_KEY='900fb6004e1d7a5a54750cba5b91d2b6'


class Development(Config):
    DEBUG = True


class Production(Config):
    DEBUG = False
