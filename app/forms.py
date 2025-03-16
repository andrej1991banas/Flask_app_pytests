from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class ItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=50)])
    description = StringField('Description', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Submit')