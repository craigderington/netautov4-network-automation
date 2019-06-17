import os
from kombu import Queue, Exchange

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    SECRET_KEY = os.urandom(32)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:$D1r3ct098!@localhost:3306/netauto'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', SQLITE_DB)

    CELERY_TIMEZONE = 'US/Eastern'
    CELERY_BROKER_URL = 'amqp://localhost/'
    CELERY_RESULT_BACKEND = 'rpc://'

    # define the tasks queues
    CELERY_QUEUES = (
        Queue('default', Exchange('default'), routing_key='default'),
        Queue('messages', Exchange('messages'), routing_key='get_messages'),
        Queue('locations', Exchange('locations'), routing_key='locations'),
        Queue('devices', Exchange('devices'), routing_key='devices'),
        Queue('endpoints', Exchange('endpoints'), routing_key='endpoints')
    )

    # define the task routes
    CELERY_ROUTES = {
        'get_new_messages': {'queue': 'get_messages', 'routing_key': 'get_messages'},
        'get_all_locations': {'queue': 'get_locations', 'routing_key': 'get_locations'},
        'get_all_devices': {'queue': 'get_devices', 'routing_key': 'get_devices'},
        'get_all_endpoints': {'queue': 'get_endpoints', 'routing_key': 'get_endpoints'}
    }


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_SERVER = 'server-path'
    MONGO_DB = ''


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}