from fastapi import FastAPI
from pydantic import BaseModel
from celery.result import AsyncResult
from .celery_worker import long_running_task

app = FastAPI()

class TaskRequest(BaseModel):
    x: int
    y: int

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI, Celery, and RabbitMQ learning project!"}

@app.post("/tasks", status_code=202)
def create_task(request: TaskRequest):
    """
    Creates a new long-running task.
    """
    task = long_running_task.delay(request.x, request.y)
    return {"task_id": task.id}

@app.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    """
    Retrieves the status and result of a task.
    """
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result,
        "error": str(task_result.info) if task_result.failed() else None,
    }
    return result
