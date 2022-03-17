import redis
from flask import render_template,request
from rq import Connection, Queue
from rq.job import Job

from app import app
from app.forms.classification_form import ClassificationForm
from ml.classification_utils import classify_image
from config import Configuration

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
    if request.method == 'POST':
        '''
        Implementation
        '''
        return render_template('classification_output_upload_queue.html')

    return render_template('classification_output_upload.html')