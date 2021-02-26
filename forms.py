from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length


class ProductForm(FlaskForm):
	product_name = StringField('Product Name', validators=[DataRequired(), Length(min=1, max=100)])
	quantity = IntegerField('Quantity')
	add_product = SubmitField('Add Product')

class LocationForm(FlaskForm):
	location_name = StringField('Location Name', validators=[DataRequired(), Length(min=1, max=100)])
	add_location = SubmitField('Add Location')

class MovementForm(FlaskForm):
	to_location = SelectField('To Location', coerce=int) #coerce is for the dropdown box so it considers the id of the entry made
	from_location = SelectField('From Location', coerce=int)
	product = SelectField('Product', coerce=int)
	quantity = IntegerField('Quantity')
	add_movement = SubmitField('Add Movement')	
