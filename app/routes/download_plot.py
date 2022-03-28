import io
from matplotlib.backends.backend_agg import FigureCanvasAgg
from flask import Response
import redis
from rq import Connection, Queue

from app import app
from app.utils.make_figure import make_figure
from config import Configuration

config = Configuration()

app.route('/download_plot/<string:job_id>', methods=['GET'])


def download_plot(job_id=None):

    """Returns the plot with the scores"""

    with io.BytesIO() as output:
        if job_id is not None:
            redis_url = Configuration.REDIS_URL
            redis_conn = redis.from_url(redis_url)
            with Connection(redis_conn):
                q = Queue(name=Configuration.QUEUE)
                task = q.fetch_job(job_id)

            # get the result as json
            result = dict(task.result)

            # get data from the result of the task
            labels = list(result.keys())
            data = list(result.values())

            # make the figure
            fig = make_figure(labels, data)

            # save the plot in the memory buffer
            FigureCanvasAgg(fig).print_png(output)

        return Response(
            output.getvalue(),
            mimetype="image/png",
            headers={"Content-disposition": "attachment; filename=result_plot.png"})
