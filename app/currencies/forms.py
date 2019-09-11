from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from app.models import Currency


class CurrencyForm(FlaskForm):
    name = StringField('Code devise', validators=[DataRequired()])
    description = StringField('Nom de la devise')
    default_curr = BooleanField('Devise par défaut')
    submit = SubmitField('Enregistrer')

    def validate_name(self, name):
        currency = Currency.query.filter_by(name=name.data).first()
        if currency is not None:
            raise ValidationError('Cette devise existe déjà, veuillez en choisir une autre.')

    def validate_default_curr(self, default_curr):
        if default_curr.data == True:
            currency = Currency.query.filter_by(default_curr=True).first()
            if currency is not None:
                raise ValidationError('Une devise par défaut existe déjà, vous ne pouvez pas en définir une autre.')


class EditCurrencyForm(FlaskForm):
    name = StringField('Code devise', validators=[DataRequired()])
    description = StringField('Nom de la devise')
    default_curr = BooleanField('Devise par défaut')
    submit = SubmitField('Enregistrer')

    def __init__(self, original_name, *args, **kwargs):
        super(EditCurrencyForm, self).__init__(*args, **kwargs)
        self.original_name = original_name

    def validate_name(self, name):
        if name.data != self.original_name:
            currency = Currency.query.filter_by(name=self.name.data).first()
            if currency is not None:
                raise ValidationError('Cette devise existe déjà, veuillez en choisir une autre.')

    def validate_default_curr(self, default_curr):
        if default_curr.data == True:
            currency = Currency.query.filter_by(default_curr=True).first()
            print(default_curr.data)
            if currency is not None:
                raise ValidationError('Une devise par défaut existe déjà, vous ne pouvez pas en définir une autre.')
