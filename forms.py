from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import DateField, DateTimeField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField, IntegerField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError




class AddDrinkForm(FlaskForm):
	ingredient_amt=StringField('Amount')
	addmore=BooleanField('Addmore')
	update=BooleanField('Update')

	submit= SubmitField('Add')


class MyCabinetForm(FlaskForm):
	ingredient=StringField('Ingredient')
	owner=StringField('Owner')
	addmore=BooleanField('Addmore')
        submit= SubmitField('Add to Cabinet')

class ShameImageForm(FlaskForm):
        pic=FileField('Shame picture',validators=[FileAllowed(['gif','jpeg','jpg','bmp'])])
        submit= SubmitField('Save Image')

class ResponseImageForm(FlaskForm):
        pic=FileField('Response picture',validators=[FileAllowed(['gif','jpeg','jpg','bmp'])])
	response=BooleanField('Right')
        submit= SubmitField('Save Image')




class LinkImageForm(FlaskForm):
	ingredient_image=FileField('New Ingredient Image',validators=[FileAllowed(['gif'])])
	submit= SubmitField('Update Image')


class AddPumpForm(FlaskForm):
	pinout=StringField('Enter Pin')
	flow=StringField('Flow Rate(seconds per ounce)')
	submit= SubmitField('Add Pump')
	
class CreatePlayerForm(FlaskForm):
	name=StringField('Player Name')
	email=StringField('E-mail')
	
	submit= SubmitField('Add Player')

class QuestionForm(FlaskForm):
	question=StringField('Ask a question')
	submit= SubmitField('Save it')

class CreateCardForm(FlaskForm):
	ctitle=StringField('Card Title')
	question=StringField('Ask a question or Task')
	card_image=FileField('Card Image',validators=[FileAllowed(['jpg','gif','bmp','jpeg','png'])])
	submit= SubmitField('Preview')
