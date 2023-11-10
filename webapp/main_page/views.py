import os
from flask import Blueprint, current_app, render_template, Flask, flash, request, redirect, url_for
import matplotlib.pyplot as plt
from webapp.user.decorators import user_required
from webapp.config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER 
from get_orders_sql import delete_orders_data
from get_plots_and_tables import get_analysed_data
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


@blueprint.route('/data_analysis_add_data')
@user_required
def data_analysis_add_data():
    current_user_id = current_user.get_id()
    normalise_users_data(current_user_id)
    clients_data = read_csv('normalised_clients.csv')
    save_clients(clients_data)
    normalise_orders_data()
    orders_data = read_csv_orders('normalised_orders.csv')
    save_orders(orders_data, current_user_id)
    return render_template("main/data_analysis.html")


@blueprint.route('/data_analysis/<string:period>')
@user_required
def data_analysis(period='M'):
    if period == 'Y' or period == 'M' or period == 'D':
        table=get_analysed_data(period)
        table_columns = table.columns.values.tolist()
        table_values = table.values.astype(float).tolist()
        dates = table.index.values.astype(str).tolist()
        if period == 'Y':
            table_columns.insert(0, "Год")
            image_hidden = False
        elif period == 'M':
            table.plot(figsize=(15,25), subplots=True)
            plt.savefig(os.path.join('webapp/static/', 'my_plot.jpg'))
            table_columns.insert(0, "Месяц")
            image_hidden = True
        elif period == 'D':
            table.plot(figsize=(15,25), subplots=True)
            plt.savefig(os.path.join('webapp/static/', 'my_plot.jpg'))
            table_columns.insert(0, "День")
            image_hidden = True
        for i in range(len(table_values)):
            table_values[i][:-1] = [round(elem) for elem in table_values[i][:-1]]
            table_values[i][-1] = format(table_values[i][-1], '.2f')
            table_values[i].insert(0, dates[i])
        return render_template("main/data_analysis.html", table_columns = table_columns, table_values = table_values, image_hidden = image_hidden)
    else:
        return render_template("main/data_analysis.html")  
    

@blueprint.route('/<int:delete>', methods=['GET', 'POST'])
@user_required
def upload_file(delete=0):
    if delete == 1:
        current_user_id = current_user.get_id()
        delete_orders_data(current_user_id)
        flash('Записи в базе данных удалены')   
    flag = 0
    if request.method == 'POST':
        if 'file_1' not in request.files or 'file_2' not in request.files:
            flash('Недопустимый формат файла')
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
    
    return render_template("main/index.html", page_title="Подгрузите файлы", flag=flag)