from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    remember_me = BooleanField('Запомнить меня', default=True, render_kw = {'class': 'form-check-input'})
    submit = SubmitField('Отправить', render_kw={"class":"btn btn-primary"})

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
    email = StringField('Электронная почта', validators=[DataRequired(), Email()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    password2 = PasswordField('Пароль', validators=[DataRequired(), EqualTo('password')], render_kw={"class": "form-control"})
    submit = SubmitField('Отправить', render_kw={"class":"btn btn-primary"})

class EditCalendarEventForm(FlaskForm):
    event_start = DateField('Начало', format="%Y-%m-%d", validators=[DataRequired()])
    event_end = DateField('Конец', format="%Y-%m-%d", validators=[DataRequired()])
    submit = SubmitField('Подтвердить', render_kw={"class":"btn btn-light"})