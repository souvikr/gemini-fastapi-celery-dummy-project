# FastAPI, Celery, Redis, and RabbitMQ Learning Project

This project is a simple demonstration of how to integrate FastAPI with Celery for background task processing. RabbitMQ is used as the message broker, and Redis is used as the result backend. The entire application is containerized using Docker.

## Prerequisites

*   Docker
*   Docker Compose

## Architecture

The project consists of four services orchestrated by Docker Compose:

*   **`web`**: A FastAPI application that provides the API endpoints to create and check tasks.
*   **`worker`**: A Celery worker that executes the background tasks.
*   **`rabbitmq`**: The message broker that passes task messages from the `web` service to the `worker`.
*   **`redis`**: The result backend that stores the results of the tasks.

## Project Structure

```
/fastapi_celery_project
|-- app
|   |-- __init__.py
|   |-- main.py       # FastAPI application
|   |-- celery_worker.py # Celery app and task definitions
|-- Dockerfile
|-- docker-compose.yml
|-- requirements.txt
|-- README.md
```

## How to Run

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd fastapi_celery_project
    ```

2.  **Start the application:**

    ```bash
    docker-compose up -d --build
    ```

    This command will build the Docker images and start all the services in the background.

    **Note on `sudo`:** If you encounter a `permission denied` error when running `docker-compose`, you may need to run the command with `sudo`:

    ```bash
    sudo docker-compose up -d --build
    ```

    This is because the Docker daemon might be configured to only be accessible by the `root` user or users in the `docker` group.

3.  **Check the status of the containers:**

    ```bash
    docker-compose ps
    ```
    or if you used `sudo` to start the containers:
    ```bash
    sudo docker-compose ps
    ```

    You should see four containers running: `fastapi_celery_project_web_1`, `fastapi_celery_project_worker_1`, `fastapi_celery_project_redis_1`, and `fastapi_celery_project_rabbitmq_1`.

The API will be available at [http://localhost:8000](http://localhost:8000). The RabbitMQ Management UI will be available at [http://localhost:15672](http://localhost:15672) (user: `user`, pass: `password`).

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

Initially, the status will be `PENDING`. After 5 seconds, the task will complete, and the status will be `SUCCESS`.

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

## Stopping the Application

To stop the application, run:

```bash
docker-compose down
```
or if you used `sudo`:
```bash
sudo docker-compose down
```