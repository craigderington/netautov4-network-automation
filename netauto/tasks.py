import datetime
import time
import pymongo
import config
import json
import csv
import requests
from celery.signals import task_postrun
from celery.utils.log import get_task_logger
from netauto import celery, db
from netauto.models import User
from sqlalchemy import and_, between
from sqlalchemy import exc, func
from sqlalchemy import text
from io import StringIO
from datetime import timedelta

# set up our logger utility
logger = get_task_logger(__name__)


def convert_datetime_object(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def convert_utc_to_local(utcdate_obj):
    nowtimestamp = time.time()
    offset = datetime.datetime.fromtimestamp(nowtimestamp) - datetime.datetime.utcfromtimestamp(nowtimestamp)
    return utcdate_obj + offset


@celery.task(queue="get_messages", max_retires=3)
def log(message):
    """Print some log messages"""
    logger.debug(message)
    return str(message)


@task_postrun.connect
def close_session(*args, **kwargs):
    # Flask SQLAlchemy will automatically create new sessions for you from
    # a scoped session factory, given that we are maintaining the same app
    # context, this ensures tasks have a fresh session (e.g. session errors
    # won't propagate across tasks)
    db.session.remove()
