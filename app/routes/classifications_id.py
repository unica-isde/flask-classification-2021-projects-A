import redis
from rq import Connection, Queue

from app import app
from config import Configuration

config = Configuration()


@app.route('/classifications/<string:job_id>', methods=['GET'])
def classifications_id(job_id):
    """Returns the status and the result of the job identified
    by the id specified in the path."""
    redis_url = Configuration.REDIS_URL
    redis_conn = redis.from_url(redis_url)
    with Connection(redis_conn):
        q = Queue(name=Configuration.QUEUE)
        task = q.fetch_job(job_id)

    response = {
        'task_status': task.get_status(),
        'data': task.result,
    }
    return response
