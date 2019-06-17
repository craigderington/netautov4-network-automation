from celery import Celery
from celery.schedules import crontab
from datetime import datetime, timedelta
from netauto import create_app
from netauto.tasks import log, get_locations

def create_celery(app):
    celery = Celery(app.import_name,
                    backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


flask_app = create_app()
celery = create_celery(flask_app)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    time_now = datetime.now()
    # period task executes every 10 seconds
    # sender.add_periodic_task(60.0, log.s(('The time is now: {}'.format(time_now.strftime('%c')))), name='Log Message Every 60')
    sender.add_periodic_task(15.0, get_locations, name="Get BBI Locations")
    # periodic task executes every 2 hours (7200)
    # periodic task executes every 4 hours (14400)
    sender.add_periodic_task(14400.0, log.s(("The time is now: {}".format(time_now.strftime("%c")))), name="Log every 4 hours")
    # periodic task to execute every 6 hours (21600)
    # periodic tasks executes every 8 hours (28800)
    sender.add_periodic_task(28800.0, log.s(("The time is now: {}".format(time_now.strftime("%c")))), name="Log every 8 hours")
    # periodic task executes every 12 hours (43200)
    # periodic task executes every 24 hours (86400)

    # periodic task executes on crontab schedule
    sender.add_periodic_task(
        crontab(hour=0, minute=2),
        sender.add_periodic_task(60.0, log.s(("The time is now: {}".format(time_now.strftime("%c")))), name="Log every 2 minutes after midnight"),
        name="Log Message on Cron schedule"
    )
