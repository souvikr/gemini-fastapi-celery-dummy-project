import time
import os
from celery import Celery

# Get broker and backend URLs from environment variables, with defaults for local development
BROKER_URL = os.environ.get("CELERY_BROKER_URL", "amqp://user:password@localhost:5672//")
BACKEND_URL = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

# Configure Celery
celery_app = Celery(
    'tasks',
    broker=BROKER_URL,
    backend=BACKEND_URL
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
