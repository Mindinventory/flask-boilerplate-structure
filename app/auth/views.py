import uuid
from functools import wraps

from flask import render_template, \
    flash, session, redirect, url_for, abort
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import check_password_hash, generate_password_hash

from app import app
from app import db
from app.auth.forms import *
from app.auth.models import User
from app.toolbox import email

# Serializer for generating random tokens
tkn = URLSafeTimedSerializer(app.config['SECRET_KEY'])


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            auth = session['email']
        except:
            auth = None
        if auth is None:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)

    return decorated_function


def index_view():
    return render_template('pages/index.html')


def signup_view():
    form = SignupForm()
    if form.validate_on_submit():
        mail = form.email.data
        user = User.query.filter_by(email=mail).first()

        if user:  # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))
        else:
            # Create a user who hasn't validated his email address
            user = User(
                public_id=str(uuid.uuid4()),
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=generate_password_hash(form.password.data),
            )
            # Insert the user in the database
            db.session.add(user)
            db.session.commit()
            # Subject of the confirmation email
            subject = 'Please confirm your email address.'
            # Generate a random token
            token = tkn.dumps(user.email, salt='email-confirm-key')
            # Build a confirm link with token
            confirmUrl = url_for('auth.confirm', token=token, _external=True)
            # Render an HTML template to send by email
            html = render_template('email/confirm.html',
                                   confirm_url=confirmUrl)
            # Send the email to user
            email.send(user.email, subject, html)
            # Send back to the home page
            flash('Check your emails to confirm your email address.', 'positive')
            return redirect(url_for('auth.signup'))
    return render_template('forms/signup.html', form=form)


def confirm_view(token):
    try:
        mail = tkn.loads(token, salt='email-confirm-key', max_age=86400)
    # The token can either expire or be invalid
    except:
        abort(404)
    # Get the user from the database
    user = User.query.filter_by(email=mail).first()
    # The user has confirmed his or her email address
    user.confirmation = True
    # Update the database with the user
    db.session.commit()
    # Send to the login page
    flash(
        'Your email address has been confirmed, you can login.', 'positive')
    return redirect(url_for('auth.login'))


def login_view():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Check the user exists
        if user is not None:
            # Check the password is correct
            if check_password_hash(user.password, form.password.data):
                session['login'] = True
                session['id'] = user.id
                session['email'] = user.email
                # Send back to the home page
                return redirect(url_for('auth.account'))
            else:
                flash('The password you have entered is wrong.', 'negative')
                return redirect(url_for('auth.login'))
        else:
            flash('Unknown email address.', 'negative')
            return redirect(url_for('auth.login'))
    return render_template('forms/login.html', form=form)



def logout_view():
    session.pop('login', None)
    session.pop('id', None)
    session.pop('email', None)
    flash('Successfully logout.', 'positive')
    return redirect(url_for('auth.login'))


@login_required
def account_view():
    mail = session['email']
    user = User.query.filter_by(email=mail).first()
    name = user.first_name
    return render_template('forms/account.html', name=name)


def forgot_view():
    form = ForgotForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Check the user exists
        if user is not None:
            # Subject of the confirmation email
            subject = 'Reset your password.'
            # Generate a random token
            token = tkn.dumps(user.email, salt='password-reset-key')
            # Build a reset link with token
            resetUrl = url_for('auth.reset', token=token, _external=True)
            # Render an HTML template to send by email
            html = render_template('email/reset.html', reset_url=resetUrl)
            # Send the email to user
            email.send(user.email, subject, html)
            # Send back to the home page
            flash('Check your emails to reset your password.', 'positive')
            return redirect(url_for('auth.login'))
        else:
            flash('Unknown email address.', 'negative')
            return redirect(url_for('auth.forgot'))
    return render_template('forms/forgot.html', form=form)


def reset_view(token):
    try:
        mail = tkn.loads(token, salt='password-reset-key', max_age=86400)
    # The token can either expire or be invalid
    except:
        abort(404)
    form = ResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=mail).first()
        # Check the user exists
        if user is not None:
            user.password = generate_password_hash(form.password.data)
            # Update the database with the user
            db.session.commit()
            # Send to the login page
            flash('Your password has been reset, you can login.', 'positive')
            return redirect(url_for('auth.login'))
        else:
            flash('Unknown email address.', 'negative')
            return redirect(url_for('auth.forgot'))
    return render_template('forms/reset.html', form=form, token=token)
