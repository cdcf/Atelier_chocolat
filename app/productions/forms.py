from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField, DateField
from wtforms.validators import DataRequired, Length
import datetime


class ProductionForm(FlaskForm):
    name = StringField('Description', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], format='%d/%m/%Y', default=datetime.date.today(),
                     id='date_picker')
    comment = TextAreaField('Commentaires', validators=[Length(min=0, max=256)])
    submit = SubmitField('Enregistrer')


class EditProductionForm(FlaskForm):
    name = StringField('Description', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], format='%d/%m/%Y', default=datetime.date.today(),
                     id='date_picker')
    comment = TextAreaField('Commentaires', validators=[Length(min=0, max=256)])
    submit = SubmitField('Enregistrer')


class ListProductionForm(FlaskForm):
    date_from = DateField('Du', format='%d/%m/%Y', validators=[DataRequired()], id='from_date_picker')
    date_to = DateField('Au', format='%d/%m/%Y', validators=[DataRequired()], id='to_date_picker')
    submit = SubmitField('Rechercher')
