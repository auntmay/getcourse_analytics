import os
from flask import Blueprint, current_app, render_template, Flask, flash, request, redirect, url_for
from webapp.user.decorators import user_required
from webapp.config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER 
from normalise_users_data import normalise_users_data
from normalise_orders_data import normalise_orders_data
from load_clients import read_csv, save_clients
from load_orders import read_csv as read_csv_orders
from load_orders import save_orders
from flask_login import current_user

blueprint = Blueprint('main_page', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@blueprint.route('/start_page')
@user_required
def start():
    return render_template("main/start_page.html")


@blueprint.route('/data_analysis')
@user_required
def data_analysis():
    current_user_id = current_user.get_id()
    normalise_users_data(current_user_id)
    clients_data = read_csv('normalised_clients.csv')
    save_clients(clients_data)
    normalise_orders_data()
    orders_data = read_csv_orders('normalised_orders.csv')
    save_orders(orders_data)
    return render_template("main/data_analysis.html")
    

@blueprint.route('/', methods=['GET', 'POST'])
@user_required
def upload_file():
    flag = 0
    if request.method == 'POST':
        if 'file_1' not in request.files or 'file_2' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file_users = request.files['file_1']
        file_orders = request.files['file_2']
        if file_users.filename == '' and file_orders.filename == '':
            flash('Файлы не добавлены')
            return redirect(request.url)
        if file_users and allowed_file(file_users.filename):
            filename = "fake_clients.csv"
            file_users.save(os.path.join(UPLOAD_FOLDER, filename))
            flag += 1
        if file_orders and allowed_file(file_orders.filename):
            filename = "fake_orders.csv"
            file_orders.save(os.path.join(UPLOAD_FOLDER, filename))
            flag += 1
    return render_template("main/index.html", page_title = "Подгрузите файлы", flag = flag)
