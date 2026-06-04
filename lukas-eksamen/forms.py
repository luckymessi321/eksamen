from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    age = StringField("Age")
    gender = StringField("Gender")
    nationality = StringField("Nationality")
    city = StringField("City")
    email = StringField("Email")
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Log in")

class LogoutForm(FlaskForm):
    submit = SubmitField("Log out")

class EditForm(FlaskForm):
    username1 = StringField("Confirm Username", validators=[InputRequired()])
    password1 = PasswordField("Confirm Password", validators=[InputRequired()])
    editUsername = StringField("New Username", validators=[InputRequired()])
    editPassword = PasswordField("New Password", validators=[InputRequired()])
    submitEdit = SubmitField("Save changes to user")


class DeleteForm(FlaskForm):
    username2 = StringField("Confirm Username", validators=[InputRequired()])
    password2 = PasswordField("Confirm Password", validators=[InputRequired()])
    submitDelete = SubmitField("Delete current user")

class ShowData(FlaskForm):
    username3 = StringField("Confirm Username", validators=[InputRequired()])
    password3 = PasswordField("Confirm Password", validators=[InputRequired()])
    showData = SubmitField("Show saved sensitive data")