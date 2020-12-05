from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, BooleanField, TextAreaField
from wtforms.validators import DataRequired

class  VideoForm(FlaskForm):
	input_file = FileField("Выберите исходный файл", validators = [DataRequired()])
	output_filename = StringField("Сохранить результат как")
	show_bbox = BooleanField("Показать обнаруженные автомобили")
	submit = SubmitField("Отправить")
