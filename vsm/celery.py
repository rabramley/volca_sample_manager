from celery import Celery
from vsm.config import BaseConfig


celery = Celery(
    'vsm',
    broker=BaseConfig.CELERY_BROKER_URL,
    backend=BaseConfig.CELERY_RESULT_BACKEND,
)


def init_celery(app):
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
