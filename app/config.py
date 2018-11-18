"""Configure application"""


class Config(object):
    """Default application configuration"""
    DEBUG = True  # Turns on debugging features in Flask
    CSRF_ENABLED = True
    SECRET_KEY = "swalehsenditapi"
    DATABASE_URL = "host='localhost' dbname='apisendit' port='5432' user='postgres' password='92203243'"


class ProductionConfig(Config):
    """Production application configuration"""
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Development application configuration"""
    DEBUG = True


class TestingConfig(Config):
    """Testing application configuration"""
    TESTING = True
    DATABASE_URL = "host='localhost' dbname='apitest' port='5432' user='postgres' password='92203243'"
