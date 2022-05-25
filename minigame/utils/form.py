from wtforms import Form, StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length, Regexp, Email


class LoginForm(Form):
    username = StringField("아이디", [InputRequired(), Length(min=4, max=20), Regexp("[a-zA-Z0-9]")])
    password = PasswordField("비밀번호", [InputRequired(), Length(min=8, max=20), Regexp("[a-zA-Z0-9]")])


class RegisterForm(Form):
    username = StringField("아이디", [InputRequired(), Length(min=4, max=20), Regexp("[a-zA-Z0-9]")])
    password = PasswordField("비밀번호", [InputRequired(), Length(min=8, max=20), Regexp("[a-zA-Z0-9]")])
    email = EmailField("이메일", [InputRequired(), Email()])
