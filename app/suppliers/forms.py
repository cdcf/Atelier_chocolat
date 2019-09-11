from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, URL
from app.models import Supplier


class SupplierForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()])
    address = StringField('Adresse', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    telephone = StringField('Téléphone')
    website = StringField('Site web', validators=[URL()])
    submit = SubmitField('Enregistrer')

    def validate_name(self, name):
        supplier = Supplier.query.filter_by(name=name.data).first()
        if supplier is not None:
            raise ValidationError('Ce fournisseur existe déjà, veuillez en créer un nouveau.')


class EditSupplierForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()])
    address = StringField('Adresse', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    telephone = StringField('Téléphone')
    website = StringField('Site web', validators=[URL()])
    submit = SubmitField('Enregistrer')

    def __init__(self, original_name, *args, **kwargs):
        super(EditSupplierForm, self).__init__(*args, **kwargs)
        self.original_name = original_name
