from sqlalchemy import func
from flask import render_template, flash, redirect, url_for, request, current_app, jsonify
from flask_login import current_user, login_required
from app import db
from app.productions.forms import ProductionForm, EditProductionForm, ListProductionForm, ProductionItemForm, \
    ViewProductionForm, EditProductionItemForm
from app.models import Production, ProductionItem, ProductFamily, Product
from app.productions import bp


@bp.route('/_get_products')
def _get_products():
    product_family_id = request.args.get('product_family_id', '01', type=str)
    products_id = [(row.id, row.name) for row in Product.query.filter_by(product_family_id=product_family_id).all()]
    return jsonify(products_id)


@bp.route('/add_production', methods=['GET', 'POST'])
@login_required
def add_production():
    form = ProductionForm()
    if form.validate_on_submit():
        production = Production(name=form.name.data,
                                date=form.date.data,
                                comment=form.comment.data,
                                author=current_user)
        db.session.add(production)
        db.session.commit()
        flash('Votre production a été enregistrée', 'success')
        return redirect(url_for('productions.add_production'))
    page = request.args.get('page', 1, type=int)
    pagination = current_user.my_productions().paginate(page, current_app.config['PRODUCTIONS_PER_PAGE'], False)
    productions = pagination.items
    return render_template('productions/add_production.html', title='Ajouter une Production', form=form,
                           productions=productions, pagination=pagination)


@bp.route('/edit_production/<id>', methods=['GET', 'POST'])
@login_required
def edit_production(id):
    production = Production.query.filter_by(id=id).first()
    form = EditProductionForm()
    if form.validate_on_submit():
        production.name = form.name.data
        production.date = form.date.data
        production.comment = form.comment.data
        db.session.add(production)
        db.session.commit()
        flash('Vos modifications ont bien été enregistrées', 'success')
        return redirect(url_for('productions.add_production'))
    elif request.method == 'GET':
        form.name.data = production.name
        form.date.data = production.date
        form.comment.data = production.comment
    page = request.args.get('page', 1, type=int)
    pagination = Production.query.order_by(Production.id.desc()).paginate(page, current_app.config['PRODUCTIONS_PER_PAGE'], False)
    productions = pagination.items
    return render_template('productions/edit_production.html', title='Editer une Production', form=form,
                           productions=productions, pagination=pagination, id=id)


@bp.route('/delete_production/<id>', methods=['POST'])
@login_required
def delete_production(id):
    production = Production.query.get_or_404(id)
    db.session.delete(production)
    db.session.commit()
    flash('Cette production a bien été supprimée.', 'success')
    return redirect(url_for('productions.add_production'))


@bp.route('/add_production_item', methods=['GET', 'POST'])
@login_required
def add_production_item():
    form = ProductionItemForm()
    form.product_family_id.choices = [(row.id, row.name) for row in ProductFamily.query.all()]
    form.product_id.choices = [(row.id, row.name) for row in Product.query.all()]
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        pagination = ProductionItem.query.order_by(ProductionItem.id.asc()).paginate(page, 4, False)
        production_items = pagination.items
        return render_template('productions/add_production_item.html', title='Ajouter des produits', form=form,
                               production_items=production_items, pagination=pagination)
    if form.validate_on_submit():
        production_item = ProductionItem(production_id=form.production_id.data.id,
                                         product_family_id=form.product_family_id.data.id,
                                         product_id=form.product_id.data.id,
                                         quantity=form.quantity.data)
        db.session.add(production_item)
        db.session.commit()
        flash('Les produits ont été ajoutés', 'success')
        return redirect(url_for('productions.edit_production', id=production_item.production_id))
    page = request.args.get('page', 1, type=int)
    pagination = ProductionItem.query.order_by(ProductionItem.id.asc()).paginate(page, 4, False)
    production_items = pagination.items
    return render_template('productions/add_production_item.html', title='Ajouter des produits', form=form,
                           production_items=production_items, pagination=pagination)


@bp.route('/edit_production_item/<id>', methods=['GET', 'POST'])
@login_required
def edit_production_item(id):
    production_item = ProductionItem.query.filter_by(id=id).first()
    form = EditProductionItemForm()
    form.product_family_id.choices = [(row.id, row.name) for row in ProductFamily.query.all()]
    form.product_id.choices = [(row.id, row.name) for row in Product.query.all()]
    if form.validate_on_submit():
        production_item.production_id = form.production_id.data.id
        production_item.product_family_id = form.product_family_id.data.id
        production_item.product_id = form.product_id.data.id
        production_item.quantity = form.quantity.data
        db.session.add(production_item)
        db.session.commit()
        flash('Vos modifications ont bien été enregistrées', 'success')
        return redirect(url_for('productions.view_production_item'))
    elif request.method == 'GET':
        form.production_id.data = production_item.production_production_item
        form.product_family_id.data = production_item.product_family_production_item
        form.product_id.data = production_item.product_production_item
        form.quantity.data = production_item.quantity
    page = request.args.get('page', 1, type=int)
    pagination = ProductionItem.query.order_by(ProductionItem.id.desc()).paginate(page, 4, False)
    production_items = pagination.items
    return render_template('productions/edit_production_item.html', title='Editer des produits', form=form,
                           production_items=production_items, pagination=pagination, id=id)


@bp.route('/delete_production_item/<id>', methods=['POST'])
@login_required
def delete_production_item(id):
    production_item = ProductionItem.query.get_or_404(id)
    db.session.delete(production_item)
    db.session.commit()
    flash('Ce produit a bien été supprimé.', 'success')
    return redirect(url_for('productions.add_production_item'))


@bp.route('/view_production_item', methods=['GET', 'POST'])
@login_required
def view_production_item():
    production_item_search = ProductionItem.query.order_by(ProductionItem.production_id.asc(),
                                                           ProductionItem.product_family_id.asc())
    form = ViewProductionForm()
    if form.validate_on_submit():
        production = form.production_id.data
        production_item_search = production_item_search.filter(ProductionItem.production_id == production.id)
    page = request.args.get('page', 1, type=int)
    pagination = production_item_search.paginate(page, 6, False)
    production_items = pagination.items
    return render_template('productions/view_production_item.html', title='Afficher une production',
                           production_items=production_items, pagination=pagination, form=form)


@bp.route('/list_of_productions', methods=['GET', 'POST'])
@login_required
def list_of_productions():
    production_search = Production.query.order_by(Production.id.desc())
    form = ListProductionForm()
    if form.validate_on_submit():
        date_from = form.date_from.data
        date_to = form.date_to.data
        production_search = production_search.filter(func.date(Production.date) >= date_from,
                                                     func.date(Production.date) <= date_to)
    page = request.args.get('page', 1, type=int)
    pagination = production_search.paginate(page, current_app.config['PRODUCTIONS_PER_PAGE'], False)
    productions = pagination.items
    return render_template('productions/list_of_productions.html', title='Liste des Productions',
                           productions=productions, pagination=pagination, form=form)


@bp.route('/my_productions', methods=['GET', 'POST'])
@login_required
def my_productions():
    production_search = current_user.my_productions()
    form = ListProductionForm()
    if form.validate_on_submit():
        date_from = form.date_from.data
        date_to = form.date_to.data
        production_search = production_search.filter(func.date(Production.date) >= date_from,
                                                     func.date(Production.date) <= date_to)
    page = request.args.get('page', 1, type=int)
    pagination = production_search.paginate(page, current_app.config['PRODUCTIONS_PER_PAGE'], False)
    productions = pagination.items
    return render_template('productions/my_productions.html', title='Mes productions', productions=productions,
                           pagination=pagination, form=form)
