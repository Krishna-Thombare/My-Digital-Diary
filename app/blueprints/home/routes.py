from flask import render_template
from . import home_bp
from app.forms.auth_forms import LoginForm, RegisterForm

@home_bp.route('/')
def home():
    login_form = LoginForm()
    register_form = RegisterForm()
    return render_template('home/home.html', login_form=login_form, register_form=register_form)
