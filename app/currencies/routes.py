from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required
from app import db
from app.currencies import bp
from app.currencies.forms import CurrencyForm, EditCurrencyForm
from app.models import Currency

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(error, 'danger')

@bp.route('/add_currency', methods=['GET', 'POST'])
@login_required
def add_currency():
    form = CurrencyForm()
    if form.validate_on_submit():
        currency = Currency(name=form.name.data,
                            description=form.description.data,
                            default_curr=form.default_curr.data)
        db.session.add(currency)
        db.session.commit()
        flash('Votre devise a bien été créée', 'success')
        return redirect(url_for('currencies.add_currency'))
    elif request.method != "GET":
        flash_errors(form)
    page = request.args.get('page', 1, type=int)
    pagination = Currency.query.order_by(Currency.name.asc()).paginate(page, current_app.config['CURRENCIES_PER_PAGE'], False)
    currencies = pagination.items
    return render_template('currencies/add_currency.html', title='Ajouter une Devise', form=form,
                           currencies=currencies, pagination=pagination)


@bp.route('/edit_currency/<id>', methods=['GET', 'POST'])
@login_required
def edit_currency(id):
    currency = Currency.query.filter_by(id=id).first()
    form = EditCurrencyForm(currency.name)
    if form.validate_on_submit():
        currency.name = form.name.data
        currency.description = form.description.data
        currency.default_curr = form.default_curr.data
        db.session.add(currency)
        db.session.commit()
        flash('Vos modifications ont bien été enregistrées.', 'success')
        return redirect(url_for('currencies.edit_currency', id=id))
    elif request.method == 'GET':
        form.name.data = currency.name
        form.description.data = currency.description
        form.default_curr.data = currency.default_curr
    else:
        flash_errors(form)
    page = request.args.get('page', 1, type=int)
    pagination = Currency.query.order_by(Currency.name.asc()).paginate(page, current_app.config['CURRENCIES_PER_PAGE'], False)
    currencies = pagination.items
    return render_template('currencies/edit_currency.html', title='Editer une devise', form=form,
                           currencies=currencies, pagination=pagination, id=id)


@bp.route('/delete_currency/<id>', methods=['POST'])
@login_required
def delete_currency(id):
    currency = Currency.query.get_or_404(id)
    db.session.delete(currency)
    db.session.commit()
    flash('La devise a bien été supprimée.', 'success')
    return redirect(url_for('currencies.list_of_currencies'))


@bp.route('/list_of_currencies')
@login_required
def list_of_currencies():
    page = request.args.get('page', 1, type=int)
    pagination = Currency.query.order_by(Currency.name.asc()).paginate(page, current_app.config['CURRENCIES_PER_PAGE'], False)
    currencies = pagination.items
    return render_template('currencies/list_of_currencies.html', title='Liste des devises',
                           currencies=currencies, pagination=pagination)
