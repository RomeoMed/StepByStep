from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField, validators
from wtforms.validators import DataRequired, EqualTo, Length, email
from wtforms.widgets import TextArea
from flask_uploads import UploadSet, IMAGES
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields.html5 import EmailField

# Set your classes here.

images = UploadSet('images', IMAGES)


class RegisterForm(FlaskForm):
    name = StringField(
        'First Name', validators=[DataRequired(), Length(min=6, max=25)]
    )

    lname = StringField(
        'Last Name', validators=[DataRequired(), Length(min=6, max=25)]
    )

    email = EmailField(
        'Email', validators=[DataRequired(), validators.email(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )

    address1 = StringField(
        'Address',
        validators=[DataRequired(), Length(min=6, max=80)]
    )

    address2 = StringField(
        'Apt #',
        validators=[Length(min=6, max=80)]
    )

    city = StringField(
        'City',
        validators=[DataRequired(), Length(min=6, max=80)]
    )

    state = StringField(
        'State',
        validators=[DataRequired(), Length(min=2, max=2)]
    )

    zip = StringField(
        'Zip',
        validators=[DataRequired(), Length(min=5, max=10)]
    )


class SecurityQuestions(FlaskForm):
    question1 = SelectField('Question 1', choices=[], coerce=int)
    answer1 = StringField(
        id='answer1',
        validators=[DataRequired(), Length(min=3, max=80)]
    )
    question2 = SelectField('Question 2', choices=[], coerce=int)
    answer2 = StringField(
        id='answer2',
        validators=[DataRequired(), Length(min=3, max=80)]
    )
    question3 = SelectField('Question 3', choices=[], coerce=int)
    answer3 = StringField(
        id='answer3',
        validators=[DataRequired(), Length(min=3, max=80)]
    )


class LoginForm(FlaskForm):
    name = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(FlaskForm):
    email = StringField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )


class BookWriter(FlaskForm):
    content = StringField(
        widget=TextArea(),
        validators=[DataRequired()]
    )
    upload = FileField('Image Upload',
        validators=[
        FileRequired(),
        FileAllowed(images, 'Images only!')]
    )


class BookSetup(FlaskForm):
    title = StringField(
        label="Title",
        description="Enter your book's title",
        validators=[DataRequired()]
    )
    acknowledgement = StringField(
        label="Acknowledgement",
        widget=TextArea(),
        description="You can also enter an acknowledgement if you wish to!"
    )


class UploadForm(FlaskForm):
    upload = FileField('Image Upload', validators=[
        FileRequired(),
        FileAllowed(images, 'Images only!')],
        )
