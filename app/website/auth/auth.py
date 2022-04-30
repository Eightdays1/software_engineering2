from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.models import User
from website.validate import Validate
from werkzeug.security import generate_password_hash
from website import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if user.check_password(password):
                flash('Successfully logged in.', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.dashboard'))
            else:
                flash('Incorrect password, please try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", current_user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if Validate(email).email() is False:
            flash('Please enter a valid email address.', category='error')
        elif user:
            flash('Email already exists.', category='error')
        elif Validate(first_name).name() is False:
            flash('Please enter a valid name', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif Validate(password1).password() is False:
            flash('password does not meet the requirements. '
                  '(Minimum eight characters, at least one letter, one number and one special character)',
                  category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created.', category='success')
            return redirect(url_for('views.dashboard'))

    return render_template("sign_up.html", current_user=current_user)

