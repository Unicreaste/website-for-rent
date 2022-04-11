from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField, PasswordField, IntegerField, FileField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Електронная почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторить пароль', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    avatar = FileField('Аватар', validators=[DataRequired()])
    tel_num = IntegerField('Номер телефона', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    submit = SubmitField('Submit')
