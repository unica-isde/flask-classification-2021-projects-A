from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired

from app.utils.list_images import list_images
from config import Configuration

conf = Configuration()


class HistogramForm(FlaskForm):
    image = SelectField('image', choices=list_images(), validators=[DataRequired()])
    submit = SubmitField('Submit')
