import os
from kombu import Queue, Exchange

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    SECRET_KEY = os.urandom(32)   

    CELERY_TIMEZONE = "US/Eastern"
    CELERY_ACCEPT_CONTENT = ["json", "yaml"]

    # define the tasks queues
    CELERY_QUEUES = (
        Queue("default", Exchange("netauto"), routing_key="default"),
        Queue("locations", Exchange("netauto"), routing_key="netauto.tasks.locations"),
        Queue("devices", Exchange("netauto"), routing_key="netauto.tasks.devices"),
        Queue("endpoints", Exchange("netauto"), routing_key="netauto.tasks.endpoints")
    )

    # define the task routes
    CELERY_ROUTES = {
        "default": {"queue": "default", "routing_key": "default"},
        "get_locations": {"queue": "locations", "routing_key": "netauto.tasks.locations"},
        "get_devices": {"queue": "devices", "routing_key": "netauto.tasks.devices"},
        "get_endpoints": {"queue": "endpoints", "routing_key": "netauto.tasks.endpoints"}
    }


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:yufakay3!@localhost:3306/netauto"
    SQLALCHEMY_DATABASE_URI = "sqlite:////netauto.db"
    
    CELERY_BROKER_URL = "pyamqp://0.0.0.0:5672/"
    CELERY_RESULT_BACKEND = "redis://0.0.0.0:6379/0"
    
    MONGO_SERVER = "0.0.0.0:27017"
    MONGO_DB = "netauto"


class DockerConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:////netauto.db"
    
    CELERY_BROKER_URL = "pyamqp://172.17.0.2:5672/"
    CELERY_RESULT_BACKEND = "redis://172.17.0.3:6379/0"
    
    MONGO_SERVER = "172.17.0.5:27017"
    MONGO_DB = "netauto"


class DockerComposeConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://username:password@mysql:3306/netauto"
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", SQLITE_DB)

    CELERY_TIMEZONE = "US/Eastern"
    CELERY_BROKER_URL = "pyamqp://rabbitmq:5672/"
    CELERY_RESULT_BACKEND = "redis://redis:6379/0"
    
    MONGO_SERVER = "database:27017"
    MONGO_DB = "netauto"


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "docker": DockerConfig,
    "docker-compose": DockerComposeConfig
}
