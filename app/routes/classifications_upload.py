import redis
from flask import render_template, request, redirect, flash
from rq import Connection, Queue
from rq.job import Job

from app import app
from app.forms.classification_form import ClassificationForm
from ml.classification_utils import classify_image
from config import Configuration
from app.utils.classifications_upload_utils import is_allowed_file,save_image

config = Configuration()


@app.route('/classifications_image_upload', methods=['GET', 'POST'])
def classifications_image_upload():
    """
    API for upload an image,
    allows the user to select an image from the computer,
    and running a
    classification job. Returns the output scores from the
    model.
    """
    form = ClassificationForm()
    if request.method == 'POST':

        if 'upload_image' not in request.files:
            flash('No image uploaded\nUpload an image to continue')
            return redirect(request.url)

        upload_image = request.files['upload_image']
        filename = upload_image.filename

        if upload_image and is_allowed_file(filename):
            save_image(upload_image)
        else:
            flash('The image uploaded is not valid\nInsert a valid image to continue')
            return redirect(request.url)

        model_id = form.model.data
        redis_url = Configuration.REDIS_URL
        redis_conn = redis.from_url(redis_url)
        with Connection(redis_conn):
            q = Queue(name=Configuration.QUEUE)
            job = Job.create(classify_image, kwargs={
                "model_id": model_id,
                "img_id": filename,
            })
            task = q.enqueue_job(job)

        # returns the image classification output from the specified model
        return render_template("classification_output_upload_queue.html",image_id=filename, jobID=task.get_id())

    return render_template('classifications_upload_select.html', form=form)
