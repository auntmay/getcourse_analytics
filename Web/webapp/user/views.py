from flask import Blueprint, Flask, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User
from webapp.db import db

blueprint = Blueprint('user', __name__, url_prefix='/users')

@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_page.start'))
    title = "Авторизация"
    login_form = LoginForm()
    return render_template("user/login.html", page_title = title, form = login_form)

@blueprint.route('/process-login', methods = ['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():                  #Если кнопка отправить нажата
        user = User.query.filter(User.userename == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы успешно вошли на сайт')
            return redirect(url_for('main_page.start'))
        
    flash('Неправильные имя или пароль')
    return redirect(url_for('user.login'))

@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('main_page.start'))

@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_page.start'))
    title = "Регистрация"
    registration_form = RegistrationForm()
    return render_template("user/registration.html", page_title = title, form = registration_form)

@blueprint.route('/process-reg', methods = ['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        news_user = User(userename=form.username.data, email=form.email.data, role='user')
        news_user.set_password(form.password.data)
        db.session.add(news_user)
        db.session.commit()
        flash('Вы успешно зарегистрированы')
        return redirect(url_for('user.login'))
    flash('Пожалуйста исправьте ошибки')
    return redirect(url_for('user.register'))