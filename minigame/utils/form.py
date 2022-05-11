from wtforms import Form, StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length, Email, Regexp


class LoginForm(Form):
    username = StringField("아이디", [InputRequired(), Length(min=4, max=20)])
    password = PasswordField("비밀번호", [InputRequired(), Length(min=4, max=20)])


class RegisterForm(Form):
    username = StringField("아이디", [InputRequired(), Length(max=20)])
    password = PasswordField("비밀번호", [InputRequired(), Length(max=20)])
    email = EmailField("이메일", [InputRequired(), Email()])
