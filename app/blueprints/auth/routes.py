from flask import render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth_bp
from app.forms.auth_forms import LoginForm, RegisterForm
from app.models import db, User

# Helper route
@auth_bp.route('/')
def home_with_forms():
    login_form = LoginForm()
    register_form = RegisterForm()
    return render_template('home/home.html', login_form=login_form, register_form=register_form)

# Register
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    session.pop('_flashes', None)
    
    if register_form.validate_on_submit():
        if User.query.filter_by(username=register_form.username.data).first():
            flash('Username already taken', 'error')
            return redirect(url_for('auth.home_with_forms'))
        
        hashed_pw = generate_password_hash(register_form.password.data)
        new_user = User(username=register_form.username.data, password=hashed_pw)
        
        db.session.add(new_user)
        db.session.commit()
        flash('Registered successfully! Please Login.', 'success')
        return redirect(url_for('auth.home_with_forms'))
    
    return redirect(url_for('auth.home_with_forms'))

# Login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    register_form = RegisterForm()
    session.pop('_flashes', None)
    
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        
        if user and check_password_hash(user.password, login_form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('journal.journal_list'))
        
        flash('Invalid username or password')
    
    return render_template('home/home.html', login_form=login_form, register_form=register_form)

# Logout
@auth_bp.route('/logout')
def logout():
    session.clear()
    session.pop('_flashes', None)
    flash('Logged out successfully!', 'info')
    return redirect(url_for('home.home'))


    
