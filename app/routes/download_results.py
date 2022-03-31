from flask import Response, json
import redis
from rq import Connection, Queue

from app import app
from config import Configuration


config = Configuration()


@app.route('/download_results/<string:job_id>', methods=['GET'])
def download_results(job_id=None):
    """Returns a JSON file with the results."""

    # default output
    result = {'Error': 'Result has expired'}

    if job_id is not None:
        redis_url = Configuration.REDIS_URL
        redis_conn = redis.from_url(redis_url)
        with Connection(redis_conn):
            q = Queue(name=Configuration.QUEUE)
            task = q.fetch_job(job_id)
        # get the result as json
        result = dict(task.result)

    return Response(
        json.dumps(result),
        mimetype="text/json",
        headers={"Content-disposition": "attachment; filename=result.json"})
