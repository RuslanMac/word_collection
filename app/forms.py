from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, \
	SubmitField, SelectField, SelectMultipleField, TextAreaField
from wtforms.validators import ValidationError,  DataRequired, Email, EqualTo, \
	Length
from app.models import User
from flask_babel import _ , lazy_gettext as _l
class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


class RegistrationForm(FlaskForm):
	username = StringField(_l('Username'), validators=[DataRequired()])
	email = StringField(_l('Email' ),validators=[DataRequired(), Email()])
	password = PasswordField(_l('Password'), validators=[DataRequired()])
	password2 = PasswordField(
		_l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
	my_language = SelectField(_l('My language'), coerce=int)
	#languages = SelectField('Foreign language', coerce=int)
	languages1 = SelectMultipleField(_l('Foreign Languages'), coerce=int)
	submit = SubmitField(_l('Register'))




	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError(_('Please use a different username.'))

	def validate_email(self, email):
		user = User.query.filter_by(email = email.data).first()
		if user is not None:
			raise ValidationError(_('Please use a different email address.'))


class DictionaryForm(FlaskForm):
	foreign_languages = SelectField('Languages', coerce=int)
	submit = SubmitField()



class AddWordForm(FlaskForm):
	languages = SelectField(_l('Language'), coerce=int)
	submit = SubmitField(_l('Add word') )
	

class EditProfileForm(FlaskForm):
	username = StringField(_l('Username'), validators=[DataRequired()])
	languages = SelectField(_l('Foreign language'), coerce=int)
	submit = SubmitField(_l('Submit'))

	def __init__(self,original_username, *args, **kwargs):
		super(EditProfileForm,self).__init__(*args,**kwargs)
		self.original_username = original_username

	def validate_username(self, username):
		if username.data != self.original_username:
			user = User.query.filter_by(username=username.data).first()
			if user is not None:
				raise ValidationError(_('Please use a different username.'))

class NewsSearchForm(FlaskForm):
	languages = SelectField(_l('Language'))
	topic = SelectField(_l('Topic'))
	submit = SubmitField(_l('Submit'))


