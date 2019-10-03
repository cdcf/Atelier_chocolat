from sqlalchemy import func
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required
from app import db
from app.products import bp
from app.products.forms import ProductForm, EditProductForm, ViewProductForm
from app.models import Product, ProductFamily


@bp.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data,
                          origin=form.origin.data,
                          organic=form.organic.data,
                          fair_trade=form.fair_trade.data,
                          crop=form.crop.data,
                          comment=form.comment.data,
                          colour=form.colour.data,
                          product_family_id=form.product_family_id.data.id)
        db.session.add(product)
        db.session.commit()
        flash('Le produit a été créé.', 'success')
        return redirect(url_for('products.add_product'))
    page = request.args.get('page', 1, type=int)
    pagination = Product.query.order_by(Product.product_family_id.asc(), Product.name.asc()).paginate(
        page, current_app.config['PRODUCTS_PER_PAGE'], False)
    products = pagination.items
    return render_template('products/add_product.html', title='Ajouter un Produit', form=form, products=products,
                           pagination=pagination)


@bp.route('/edit_product/<id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.filter_by(id=id).first()
    form = EditProductForm(product.name)
    if form.validate_on_submit():
        product.name = form.name.data
        product.origin = form.origin.data
        product.organic = form.organic.data
        product.fair_trade = form.fair_trade.data
        product.crop = form.crop.data
        product.comment = form.comment.data
        product.colour = form.colour.data
        product.product_family_id = form.product_family_id.data.id
        db.session.add(product)
        db.session.commit()
        flash('Vos modifications ont été enregistrées.', 'success')
        return redirect(url_for('products.list_of_products'))
    elif request.method == 'GET':
        form.product_family_id.data = product.product_product
        form.name.data = product.name
        form.origin.data = product.origin
        form.organic.data = product.organic
        form.fair_trade.data = product.fair_trade
        form.crop.data = product.crop
        form.comment.data = product.comment
        form.colour.data = product.colour
    page = request.args.get('page', 1, type=int)
    pagination = Product.query.order_by(Product.product_family_id.asc(), Product.name.asc()).paginate(
        page, current_app.config['PRODUCTS_PER_PAGE'], False)
    products = pagination.items
    return render_template('products/edit_product.html', title='Edit a Product', form=form, products=products,
                           pagination=pagination, id=id)


@bp.route('/delete_product/<id>', methods=['POST'])
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Le produit a été supprimé.', 'success')
    return redirect(url_for('products.add_product'))


@bp.route('/list_of_products')
@login_required
def list_of_products():
    page = request.args.get('page', 1, type=int)
    pagination = Product.query.order_by(Product.product_family_id.asc(), Product.name.asc()).paginate(
        page, current_app.config['PRODUCTS_PER_PAGE'], False)
    products = pagination.items
    return render_template('products/list_of_products.html', title='List des produits', products=products,
                           pagination=pagination)
