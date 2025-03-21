import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import generate_password_hash, check_password_hash

from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']

        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        if not password:
            error = 'Password is required.'
        if not email:
            error = 'Email is required.'
        if confirm_password != password:
            error = 'Passwords do not match.'

        if error is None:
            try:
                db.execute(
                    'INSERT INTO user (username, password, email) VALUES (?, ?, ?)',
                    (username, generate_password_hash(password), email),
                )
                db.commit()
            except db.IntegrityError:
                error = f'Username {username} already in use.'
            else:
                flash('Registered successfully.', 'success')
                return redirect(url_for('auth.login'))

        flash(error,'error')
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_mail = request.form['user_mail']
        password = request.form['password']
        db = get_db()
        error = None

        user = db.execute('SELECT * FROM user WHERE username =? OR email =?', (user_mail, user_mail)).fetchone()

        if user is None or not check_password_hash(user['password'], password):
            error = 'Incorrect credentials.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))

        flash(error, 'error')
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view