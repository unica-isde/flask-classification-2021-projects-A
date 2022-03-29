from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired, InputRequired, NumberRange

from app.utils.list_images import list_images
from config import Configuration

conf = Configuration()


class TransformationForm(FlaskForm):

    brightness = DecimalField('brightness', validators=[NumberRange(min=0), InputRequired()], default=conf.default_brightness)
    contrast = DecimalField('contrast', validators=[NumberRange(min=0), InputRequired()], default=conf.default_contrast)
    saturation = DecimalField('saturation', validators=[NumberRange(min=0), InputRequired()], default=conf.default_saturation)
    hue = DecimalField('hue', validators=[NumberRange(min=-0.5, max=0.5), InputRequired()], default=conf.default_hue)

    image = SelectField('image', choices=list_images(), validators=[DataRequired()])
    submit = SubmitField('Submit')
