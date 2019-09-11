from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm
from app.models import User, Production
from app.main import bp


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    productions = user.productions.order_by(Production.timestamp.desc()).paginate(
        page, current_app.config['PRODUCTIONS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=productions.next_num) \
        if productions.has_next else None
    prev_url = url_for('main.user', username=user.username, page=productions.prev_num) \
        if productions.has_prev else None
    return render_template('users/user.html', user=user, productions=productions.items, next_url=next_url, prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.second_name = form.second_name.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Vos modifications ont été enregistrées.')
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.second_name.data = current_user.second_name
        form.about_me.data = current_user.about_me
    return render_template('users/edit_profile.html', title='Modifier votre profil', form=form)


@bp.route('/list_of_users')
@login_required
def list_of_users():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.username.asc()).paginate(page, 5, False)
    users = pagination.items
    return render_template('users/list_of_users.html', title='Liste des utilisateurs', users=users,
                           pagination=pagination)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Utilisateur {} non trouvé!'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('Vous ne pouvez pas vous suivre vous-même!')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('Vous suivez désormais {}!'.format(username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Utilisateur {} non trouvé!'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('Vous ne pouvez pas ne plus vous suivre!')
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('Vous ne suivez plus {}!'.format(username))
    return redirect(url_for('main.user', username=username))
