import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_messagies.settings')

app = Celery('tasks', broker='amqp://')
app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()
