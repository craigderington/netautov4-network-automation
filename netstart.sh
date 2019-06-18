#!/bin/bash

# display earl header
cat netauto.txt

# display application description
printf "Celery Distributed Asynchronous Task Queue.  A Python, Flask, Celery, SQLAlchemy & RabbitMQ Project\n\n"

# the path to the application directory
application_directory="/home/ubuntu/ebridge-network-automation"

# move to the application directory
echo "Moving to application directory $application_directory"
cd "$application_directory"

# activate the python virtual environment
echo "Activating the python virtual environment, please wait..."
source "/home/ubuntu/ebridge-network-automation/.env/bin/activate"

# start Network Automation
printf "Starting Network Automation in $application_directory on $(date)\n\n"
screen -dmS celery-beat celery -A celery_worker:celery beat --loglevel=INFO
screen -dmS get-locations celery -A celery_worker:celery worker -E -l INFO -n worker0@%h -Q locations -c 2
screen -dmS get-devices celery -A celery_worker:celery worker -E -l INFO -n worker1@%h -Q devices -c 2
screen -dmS get-endpoints celery -A celery_worker:celery worker -E -l INFO -n worker2@%h -Q endpoints -c 2

# list the Network Automation queues in screen
echo "Networking Automation successfully started..."
screen -ls


