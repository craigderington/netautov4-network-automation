import datetime
import time
import pymongo
import config
import json
import csv
import requests
from requests.auth import HTTPBasicAuth
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

# Base Objects
SNOW_BASE_URL = "https://dev73949.service-now.com/api/x_328385_restapi/bbi"
API_METHOD = "GET"
auth = HTTPBasicAuth("admin", "$GoArmy9605!")
hdrs = {"Content-Type": "application/json", "Accept": "application/json"}

def convert_datetime_object(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def convert_utc_to_local(utcdate_obj):
    nowtimestamp = time.time()
    offset = datetime.datetime.fromtimestamp(nowtimestamp) - datetime.datetime.utcfromtimestamp(nowtimestamp)
    return utcdate_obj + offset


@celery.task(queue="messages", max_retires=3)
def log(message):
    """Print some log messages"""
    logger.debug(message)
    return str(message)


@celery.task(queue="locations", max_retries=3)
def get_locations():
    """
    Get the list of Active BBI Locations
    :param: None
    :return list
    """

    resource_path = "/locations"
    store_id = None

    try: 
        # make the request
        r = requests.request(
                API_METHOD, 
                SNOW_BASE_URL + resource_path, 
                auth=auth, 
                headers=hdrs
        )

        # check for HTTP status codes other than 200
        if r.status_code != 200: 
            logger.warning('Status:', r.status_code, 'Headers:', r.headers, 'Error Response:', r.json())

        # decode the JSON response into a dictionary and use the data
        data = r.json()
        
        # ensure we have a valid data instance
        if isinstance(data, dict):
            for row in data["result"]:
                store_id = row["StoreID"]              
                # send the store ID into the next queue
                get_location_info.delay(store_id)
                logger.info("BBI Store ID: {} was sent to the Location Task Queue for processing".format(str(store_id)))
        else:
            logger.warning("The BBI API response is malformed, returned {} instead of dict".format(type(data)))

    except requests.HTTPError as http_err:
        logger.warning("BBI API Call returned error: {}".format(str(http_err)))


    return id


@celery.task(queue="locations", max_retries=3)
def get_location_info(store_id):
    """
    Get each locations information by Store ID
    :param: id (int)
    :return json object
    """
    if not isinstance(store_id, int):
        try:
            store_id = int(store_id)
        except TypeError as err:
            logger.critical("The store ID parameter is an invalid type and can not be coerced to integer: {}".format(str(err)))
            return store_id

    pathParams = store_id
    resource_path = "/location/{}".format(str(pathParams))
    
    try:
        r = requests.request(
            API_METHOD, 
            SNOW_BASE_URL + resource_path, 
            headers=hdrs, 
            auth=auth
        )

        # check for HTTP status codes other than 200
        if r.status_code != 200: 
            logger.warning("Status:", r.status_code, "Headers:", r.headers, "Error Response:", r.json())

        # decode the JSON response into a dictionary and use the data
        data = r.json()

        if isinstance(data, dict):
            # send the device info into the Task Queue for processing
            get_devices.delay(store_id)
            logger.info(data)
            logger.info("BBI Network Automation send Store ID: {} into the task queue for a list of devices".format(str(store_id)))
        
        else:
            logger.warning("The BBI API Response is malformed.  Returned {} instead of dict".format(str(type(data))))

    except requests.HTTPError as http_err:
        logger.warning("API call returned error: {}".format(str(http_err)))

    return id


@celery.task(queue="devices", max_retries=3)
def get_devices(store_id):
    """
    Get the Location devices data list
    :param: id int
    :return json object
    """

    pathParams = store_id
    resource_path = "/location/{}/devices".format(str(pathParams))

    try:
        r = requests.request(
            API_METHOD,
            SNOW_BASE_URL + resource_path,
            headers=hdrs,
            auth=auth
        )
        
        # check for HTTP status codes other than 200
        if r.status_code != 200: 
            logger.warning("Status:", r.status_code, "Headers:", r.headers, "Error Response:", r.json())

        # decode the JSON response into a dictionary and use the data
        data = r.json()
        logger.info(data)

    except requests.HTTPError as http_err:
        logger.warning("API call returned error: {}".format(str(http_err)))

    return id    


@task_postrun.connect
def close_session(*args, **kwargs):
    # Flask SQLAlchemy will automatically create new sessions for you from
    # a scoped session factory, given that we are maintaining the same app
    # context, this ensures tasks have a fresh session (e.g. session errors
    # won't propagate across tasks)
    db.session.remove()
