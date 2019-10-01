from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField, DateField, DecimalField
from wtforms.validators import DataRequired, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import Product, ProductFamily, Production
import datetime


def get_productions():
    return Production.query.order_by(Production.id)


def get_product_families():
    return ProductFamily.query.order_by(ProductFamily.name)


def get_products():
    return Product.query.order_by(Product.name)


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


class ProductionItemForm(FlaskForm):
    production_id = QuerySelectField('Production', validators=[DataRequired()],
                                     query_factory=get_productions,
                                     allow_blank=True,
                                     get_label='id',
                                     blank_text=u'-- Choisissez une production --',
                                     id='select_production')
    product_family_id = QuerySelectField('Famille de Produit', validators=[DataRequired()],
                                         query_factory=get_product_families,
                                         allow_blank=True,
                                         get_label='name',
                                         blank_text=u'-- Choisissez une famille --',
                                         id='select_product_family')
    product_id = QuerySelectField('Produit', validators=[DataRequired()],
                                  query_factory=get_products,
                                  allow_blank=True,
                                  get_label='name',
                                  blank_text=u'-- Choisissez une produit --',
                                  id='select_product')
    quantity = DecimalField('Quantité', validators=[DataRequired()])
    submit = SubmitField('Ajouter')
