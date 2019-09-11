from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models import ProductFamily


class ProductFamilyForm(FlaskForm):
    name = StringField('Famille de produit', validators=[DataRequired()])
    icon = StringField('Choisissez une icone')
    submit = SubmitField('Enregistrer')

    def validate_name(self, name):
        product_family = ProductFamily.query.filter_by(name=name.data).first()
        if product_family is not None:
            raise ValidationError('La famille de produit existe déjà, veuillez en choisir une autre.')


class EditProductFamilyForm(FlaskForm):
    name = StringField('Famille de produit', validators=[DataRequired()])
    icon = StringField('Choisissez une icone')
    submit = SubmitField('Enregistrer')

    def __init__(self, original_name, *args, **kwargs):
        super(EditProductFamilyForm, self).__init__(*args, **kwargs)
        self.original_name = original_name
