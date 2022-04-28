from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, FileField, EmailField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired


class AddDepartForm(FlaskForm):
    name = StringField('Имя:', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    tel_num = StringField('Номер телефона:', validators=[DataRequired()])
    email = EmailField('Электронная почта', validators=[DataRequired()])
    img = FileField('Аватар', validators=[DataRequired()])
    submit = SubmitField('Submit')
