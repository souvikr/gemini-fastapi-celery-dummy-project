import time
from celery import Celery

# Configure Celery
celery_app = Celery(
    'tasks',
    broker='amqp://user:password@localhost:5672//',
    backend='redis://localhost:6379/0'
)

@celery_app.task
def long_running_task(x, y):
    """
    A simple task that simulates a long-running operation.
    """
    time.sleep(5)  # Simulate a 5-second task
    return x + y

# Optional: Add a simple health check task
@celery_app.task
def health_check():
    return "Celery is running!"

celery_app.conf.update(
    task_track_started=True,
)
