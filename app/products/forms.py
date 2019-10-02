from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import Product, ProductFamily


def get_product_family():
    return ProductFamily.query.order_by(ProductFamily.name)


class ProductForm(FlaskForm):
    product_family_id = QuerySelectField('Famille de Produit', validators=[DataRequired()],
                                  query_factory=get_product_family,
                                  allow_blank=True,
                                  get_label='name',
                                  blank_text=u'-- Choisissez une famille --')
    name = StringField('Produit', validators=[DataRequired()])
    origin = StringField('Origine', validators=[DataRequired()])
    organic = BooleanField('Bio')
    fair_trade = BooleanField('Equitable')
    crop = StringField('Année de récolte')
    comment = TextAreaField('Commentaires', validators=[Length(min=0, max=256)])
    colour = StringField('Choisissez une couleur')
    submit = SubmitField('Enregistrer')

    def validate_name(self, name):
        product = Product.query.filter_by(name=name.data).first()
        if product is not None:
            raise ValidationError('Le produit existe déjà, veuillez en choisir un autre.')


class EditProductForm(FlaskForm):
    product_family_id = QuerySelectField('Famille de Produit', validators=[DataRequired()],
                                           query_factory=get_product_family,
                                           allow_blank=True,
                                           get_label='name',
                                           blank_text=u'-- Choisissez une catégorie --')
    name = StringField('Produit', validators=[DataRequired()])
    origin = StringField('Origine', validators=[DataRequired()])
    organic = BooleanField('Bio')
    fair_trade = BooleanField('Equitable')
    crop = StringField('Année de récolte')
    comment = StringField('Commentaires')
    colour = StringField('Choisissez une couleur')
    submit = SubmitField('Enregistrer')

    def __init__(self, original_name, *args, **kwargs):
        super(EditProductForm, self).__init__(*args, **kwargs)
        self.original_name = original_name
