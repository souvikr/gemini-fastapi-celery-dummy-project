# FastAPI, Celery, Redis, and RabbitMQ Learning Project

This project is a simple demonstration of how to integrate FastAPI with Celery for background task processing. RabbitMQ is used as the message broker and Redis is used as the result backend.

## Project Structure

```
/fastapi_celery_project
|-- app
|   |-- __init__.py
|   |-- main.py       # FastAPI application
|   |-- celery_worker.py # Celery app and task definitions
|-- docker-compose.yml
|-- requirements.txt
|-- README.md
```

## How to Run

### 1. Start Infrastructure

First, start the Redis and RabbitMQ services using Docker Compose.

```bash
cd fastapi_celery_project
docker-compose up -d
```

You can check the status of the containers with `docker-compose ps`.
The RabbitMQ Management UI will be available at [http://localhost:15672](http://localhost:15672) (user: `user`, pass: `password`).

### 2. Set up Python Environment

It is recommended to use a virtual environment.

```bash
cd fastapi_celery_project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the Celery Worker

Open a new terminal, navigate to the project directory, activate the virtual environment, and start the Celery worker.

```bash
cd fastapi_celery_project
source venv/bin/activate
celery -A app.celery_worker worker --loglevel=info
```

### 4. Run the FastAPI Application

Open another new terminal, navigate to the project directory, activate the virtual environment, and start the FastAPI server using Uvicorn.

```bash
cd fastapi_celery_project
source venv/bin/activate
uvicorn app.main:app --reload
```

The API will be available at [http://localhost:8000](http://localhost:8000).

## How to Use

### 1. Create a Task

Send a POST request to the `/tasks` endpoint.

```bash
curl -X POST "http://localhost:8000/tasks" \
-H "Content-Type: application/json" \
-d '{"x": 5, "y": 7}'
```

This will return a `task_id`.

```json
{
  "task_id": "some-unique-task-id"
}
```

### 2. Check Task Status

Use the `task_id` to check the status of the task.

```bash
curl http://localhost:8000/tasks/some-unique-task-id
```

Initially, the status will be `PENDING`. After 5 seconds, the task will complete and the status will be `SUCCESS`.

**Pending:**
```json
{
  "task_id": "some-unique-task-id",
  "status": "PENDING",
  "result": null,
  "error": null
}
```

**Success:**
```json
{
  "task_id": "some-unique-task-id",
  "status": "SUCCESS",
  "result": 12,
  "error": null
}
```
