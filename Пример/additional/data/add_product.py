from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, DateField, FileField, TextAreaField
from wtforms.validators import DataRequired


class AddProductForm(FlaskForm):
    product_name = StringField('Название товара', validators=[DataRequired()])
    summ = IntegerField('Цена', validators=[DataRequired()])
    using = TextAreaField('Описание или примечания к товару', validators=[DataRequired()])
    img = FileField('Фото товара', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])

    submit = SubmitField('Submit')
