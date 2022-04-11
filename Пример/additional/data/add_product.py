from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, DateField, FileField
from wtforms.validators import DataRequired


class AddProductForm(FlaskForm):
    product_name = StringField('Название товара', validators=[DataRequired()])
    summ = IntegerField('Цена', validators=[DataRequired()])
    using = StringField('Описание или примечания к товару', validators=[DataRequired()])
    date = DateField('Дата', validators=[DataRequired()])
    img = FileField('Фото товара', validators=[DataRequired()])

    submit = SubmitField('Submit')
