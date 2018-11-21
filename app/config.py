"""Configure application"""


class Config(object):
    """Default application configuration"""
    DEBUG = True  # Turns on debugging features in Flask
    CSRF_ENABLED = True
    SECRET_KEY = "swalehsenditapi"
    DATABASE_URL = "postgres://onaypcbzblxgag:dd94e7345a81b81119ed1dd0c731957430ffb6a70213c50fc88e9fa837c3b26e@ec2-23-21-201-12.compute-1.amazonaws.com:5432/d6qaa62ktbru01"


class ProductionConfig(Config):
    """Production application configuration"""
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Development application configuration"""
    DEBUG = True
    DATABASE_URL = "host='localhost' dbname='apisendit' port='5432' user='postgres' password='92203243'"


class TestingConfig(Config):
    """Testing application configuration"""
    TESTING = True
    DATABASE_URL = "host='localhost' dbname='apitest' port='5432' user='postgres' password='92203243'"
