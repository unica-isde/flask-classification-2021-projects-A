import redis
from flask import render_template
from rq import Connection, Queue
from rq.job import Job
import os
from app import app
from app.forms.classification_form import ClassificationForm
from app.forms.classification_form2 import ClassificationForm2

from ml.classification_utils import classify_image,fetch_image
from config import Configuration
import matplotlib.pyplot as plt
import cv2
import numpy as np
    
config = Configuration()


@app.route('/classifications', methods=['GET', 'POST'])
def classifications():
    """API for selecting a model and an image and running a 
    classification job. Returns the output scores from the 
    model."""
    form = ClassificationForm()
    if form.validate_on_submit():  # POST
        image_id = form.image.data
        model_id = form.model.data

        redis_url = Configuration.REDIS_URL
        redis_conn = redis.from_url(redis_url)
        with Connection(redis_conn):
            q = Queue(name=Configuration.QUEUE)
            job = Job.create(classify_image, kwargs={
                "model_id": model_id,
                "img_id": image_id
            })
            task = q.enqueue_job(job)

        # returns the image classification output from the specified model
        # return render_template('classification_output.html', image_id=image_id, results=result_dict)
        return render_template("classification_output_queue.html", image_id=image_id, jobID=task.get_id())

    # otherwise, it is a get request and should return the
    # image and model selector
    return render_template('classification_select.html', form=form)






@app.route('/showhistogram', methods=['GET', 'POST'])
def showHistogram():
    """API for selecting an image and running a 
    histogram image job. Returns the original image and histogram image
    """
    form = ClassificationForm2()
    if form.validate_on_submit():  # POST
        image_id = form.image.data
        histogram_image = plot_png(image_id)

        return render_template("show_histogram.html", histogram_image=histogram_image, image_id=image_id, jobID=task.get_id())

    # otherwise, it is a get request and should return the
    # image  selector
    return render_template('show_histogramform.html', form=form)


def plot_png(imageurl):
    image_path = os.path.join(config.image_folder_path, imageurl)
    histo_path =os.path.join(config.histo_folder_path,imageurl)
    # read image
    im = cv2.imread(image_path)
    # calculate mean value from RGB channels and flatten to 1D array
    vals = im.mean(axis=2).flatten()
    # calculate histogram
    counts, bins = np.histogram(vals, range(257))
    # plot histogram centered on values 0..255
    plt.bar(bins[:-1] - 0.5, counts, width=1, edgecolor='none')
    plt.xlim([-0.5, 255.5])
    plt.savefig(histo_path)
    return imageurl
