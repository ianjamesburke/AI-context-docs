from fastapi import FastAPI
from rq import Queue, Job
from redis import Redis
import time

# Initialize the FastAPI app
app = FastAPI()

# Connect to Redis (used as the backend to manage the job queue)
redis_conn = Redis(host="localhost", port=6379, db=0)

# Create an RQ Queue instance using the Redis connection
queue = Queue(connection=redis_conn)


# Background task function (executed asynchronously in the queue)
def background_task(param: str):
    time.sleep(10)  # Simulates task processing delay
    return f"Task completed with param: {param}"


# Endpoint to enqueue a task into the Redis Queue
@app.post("/enqueue/")
def enqueue_job(param: str):
    """
    Enqueue a new job into the Redis Queue.
    :param param: The parameter to pass to the task.
    :return: A response with the job ID and its initial status.
    """
    job = queue.enqueue(background_task, param)
    return {"job_id": job.id, "status": "queued"}


# Endpoint to check the status of a specific job
@app.get("/status/{job_id}")
def get_job_status(job_id: str):
    """
    Fetch the status of a job using its ID.
    :param job_id: The unique ID of the job.
    :return: The job's ID, current status, and result (if available).
    """
    try:
        job = Job.fetch(job_id, connection=redis_conn)
        return {
            "job_id": job.id,
            "status": job.get_status(),
            "result": job.result  # Result of the job (None if not finished)
        }
    except Exception as e:
        return {"error": str(e)}


# Usage for importing and mounting this FastAPI app:
# This app can be used as a standalone service or as part of a larger FastAPI project.
# To include it in another project:
# 1. Import the `app` object from this module:
#    `from job_queue import app as job_queue_app`
# 2. Mount it to an existing FastAPI application:
#    ```
#    from fastapi import FastAPI
#    from job_queue import app as job_queue_app
#
#    main_app = FastAPI()
#    main_app.mount("/jobs", job_queue_app)
#    ```
# 3. Run the main application, and the job endpoints will be available under `/jobs`.

# Uncomment the following to run this app standalone:
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)
