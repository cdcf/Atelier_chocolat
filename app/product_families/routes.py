from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required
from app import db
from app.product_families import bp
from app.product_families.forms import ProductFamilyForm, EditProductFamilyForm
from app.models import ProductFamily


@bp.route('/add_product_family', methods=['GET', 'POST'])
@login_required
def add_product_family():
    form = ProductFamilyForm()
    if form.validate_on_submit():
        product_family = ProductFamily(name=form.name.data,
                                     icon=form.icon.data)
        db.session.add(product_family)
        db.session.commit()
        flash('La famille de produit a été créée.', 'success')
        return redirect(url_for('product_families.add_product_family'))
    page = request.args.get('page', 1, type=int)
    pagination = ProductFamily.query.order_by(
        ProductFamily.name.asc()).paginate(page, current_app.config['PRODUCT_FAMILIES_PER_PAGE'], False)
    product_families = pagination.items
    return render_template('product_families/add_product_family.html', title='Ajouter une famille de produit',
                           form=form, product_families=product_families, pagination=pagination)


@bp.route('/edit_product_family/<id>', methods=['GET', 'POST'])
@login_required
def edit_product_family(id):
    product_family = ProductFamily.query.filter_by(id=id).first()
    form = EditProductFamilyForm(product_family.name)
    if form.validate_on_submit():
        product_family.name = form.name.data
        product_family.icon = form.icon.data
        db.session.add(product_family)
        db.session.commit()
        flash('Vos modifications ont été enregistrées.', 'success')
        return redirect(url_for('product_families.list_of_product_families', id=id))
    elif request.method == 'GET':
        form.name.data = product_family.name
        form.icon.data = product_family.icon
    page = request.args.get('page', 1, type=int)
    pagination = ProductFamily.query.order_by(
        ProductFamily.name.asc()).paginate(page, current_app.config['PRODUCT_FAMILIES_PER_PAGE'], False)
    product_families = pagination.items
    return render_template('product_families/edit_product_family.html', title='Modifier une famille de produit',
                           form=form, product_families=product_families, pagination=pagination, id=id)


@bp.route('/delete_product_family/<id>', methods=['POST'])
@login_required
def delete_product_family(id):
    product_family = ProductFamily.query.get_or_404(id)
    db.session.delete(product_family)
    db.session.commit()
    flash('La famille de produit a bien été supprimée.', 'success')
    return redirect(url_for('product_families.add_product_family'))


@bp.route('/list_of_product_families')
@login_required
def list_of_product_families():
    page = request.args.get('page', 1, type=int)
    pagination = ProductFamily.query.order_by(
        ProductFamily.name.asc()).paginate(page, current_app.config['PRODUCT_FAMILIES_PER_PAGE'], False)
    product_families = pagination.items
    return render_template('product_families/list_of_product_families.html',
                           title='Liste des familles de produits', product_families=product_families,
                           pagination=pagination)
