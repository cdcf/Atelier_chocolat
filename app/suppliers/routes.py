from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required
from app import db
from app.suppliers import bp
from app.suppliers.forms import SupplierForm, EditSupplierForm
from app.models import Supplier


@bp.route('/add_supplier', methods=['GET', 'POST'])
@login_required
def add_supplier():
    form = SupplierForm()
    if form.validate_on_submit():
        supplier = Supplier(name=form.name.data,
                            address=form.address.data,
                            email=form.email.data,
                            telephone=form.telephone.data,
                            website=form.website.data)
        db.session.add(supplier)
        db.session.commit()
        flash('Le fournisseur a été créé.', 'success')
        return redirect(url_for('suppliers.add_supplier'))
    page = request.args.get('page', 1, type=int)
    pagination = Supplier.query.order_by(Supplier.name.asc()).paginate(
        page, current_app.config['SUPPLIERS_PER_PAGE'], False)
    suppliers = pagination.items
    return render_template('suppliers/add_supplier.html', title='Ajouter un fournisseur',
                           form=form, suppliers=suppliers, pagination=pagination)


@bp.route('/edit_supplier/<id>', methods=['GET', 'POST'])
@login_required
def edit_supplier(id):
    supplier = Supplier.query.filter_by(id=id).first()
    form = EditSupplierForm(supplier.name)
    if form.validate_on_submit():
        supplier.name = form.name.data
        supplier.icon = form.icon.data
        db.session.add(supplier)
        db.session.commit()
        flash('Vos modifications ont été enregistrées.', 'success')
        return redirect(url_for('suppliers.list_of_suppliers', id=id))
    elif request.method == 'GET':
        form.name.data = supplier.name
        form.address.data = supplier.address
        form.email.data = supplier.email
        form.telephone.data = supplier.telephone
        form.website.data = supplier.website
    page = request.args.get('page', 1, type=int)
    pagination = Supplier.query.order_by(Supplier.name.asc()).paginate(
        page, current_app.config['SUPPLIERS_PER_PAGE'], False)
    suppliers = pagination.items
    return render_template('suppliers/edit_supplier.html', title='Modifier un fournisseur',
                           form=form, suppliers=suppliers, pagination=pagination, id=id)


@bp.route('/delete_supplier/<id>', methods=['POST'])
@login_required
def delete_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    db.session.delete(supplier)
    db.session.commit()
    flash('Le fournisseur a bien été supprimée.', 'success')
    return redirect(url_for('suppliers.list_of_suppliers'))


@bp.route('/list_of_suppliers')
@login_required
def list_of_suppliers():
    page = request.args.get('page', 1, type=int)
    pagination = Supplier.query.order_by(
        Supplier.name.asc()).paginate(page, current_app.config['SUPPLIERS_PER_PAGE'], False)
    suppliers = pagination.items
    return render_template('suppliers/list_of_suppliers.html',
                           title='Liste des fournisseurs', suppliers=suppliers, pagination=pagination)
