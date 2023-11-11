import os
from flask import Blueprint, current_app, render_template, Flask, flash, request, redirect, url_for
import matplotlib.pyplot as plt
from webapp.user.decorators import user_required
from webapp.config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER 
from get_orders_table import delete_orders_data
from get_plots_and_tables import get_analysed_data
from normalise_users_data import normalise_users_data
from normalise_orders_data import normalise_orders_data
from load_clients import read_csv, save_clients
from load_orders import read_csv as read_csv_orders
from load_orders import save_orders
from load_expences import read_csv as read_csv_expences
from load_expences import save_expenses
from flask_login import current_user
from webapp.user.forms import EditCalendarEventForm

blueprint = Blueprint('main_page', __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def add_file(file, name, flag):
    if file and allowed_file(file.filename):
        filename = name
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        flag += 1
    return flag


@blueprint.route('/')
@user_required
def start():
    return render_template("main/start_page.html")


@blueprint.route('/data_analysis_add_data')
@user_required
def data_analysis_add_data():
    current_user_id = current_user.get_id()
    print(current_user.get_id())
    normalise_users_data(current_user_id)
    clients_data = read_csv('normalised_clients.csv')
    save_clients(clients_data)
    normalise_orders_data()
    orders_data = read_csv_orders('normalised_orders.csv')
    save_orders(orders_data, current_user_id)
    expenses_data = read_csv_expences('fake_expences.csv', current_user_id)
    save_expenses(expenses_data)
    return render_template("main/data_analysis.html")


@blueprint.route('/data_analysis/<string:period>')
@user_required
def data_analysis(period):
    if period == 'Y' or period == 'M' or period == 'D':
        current_user_id = current_user.get_id()
        try:
            table=get_analysed_data(period, current_user_id)
        except ValueError:
            flash('У вас нет записей в базе данных, добавьте файлы чтобы проанализировать данные')
            return render_template("main/index.html", page_title="Подгрузите файлы", flag=0)
        table_columns = table.columns.values.tolist()
        table_values = table.values.astype(float).tolist()
        dates = table.index.values.astype(str).tolist()
        if period == 'Y':
            table_columns.insert(0, "Год")
            image_hidden = False
        elif period == 'M':
            table.plot(figsize=(10,10), subplots=True)
            plt.savefig(os.path.join('webapp/static/', 'my_plot.jpg'))
            table_columns.insert(0, "Месяц")
            image_hidden = True
        elif period == 'D':
            table.plot(figsize=(10,10), subplots=True)
            plt.savefig(os.path.join('webapp/static/', 'my_plot.jpg'))
            table_columns.insert(0, "День")
            image_hidden = True
        for i in range(len(table_values)):
            table_values[i][:-1] = [round(elem) for elem in table_values[i][:-1]]
            table_values[i][-1] = format(table_values[i][-1], '.2f')
            table_values[i].insert(0, dates[i])
            range_hidden = False
        return render_template("main/data_analysis.html", table_columns=table_columns, table_values=table_values, range_hidden=range_hidden, image_hidden=image_hidden)
    elif period == 'R':
        range_hidden = True
        allowed_dates = EditCalendarEventForm()
        return render_template("main/data_analysis.html", range_hidden=range_hidden, form=allowed_dates)
    return render_template("main/data_analysis.html")  
    

@blueprint.route('/data_analysis_range', methods = ['POST'])
@user_required
def data_analysis_range():
    allowed_dates = EditCalendarEventForm()
    current_user_id = current_user.get_id()
    try:
        table=get_analysed_data('D', current_user_id)
    except ValueError:
        flash('У вас нет записей в базе данных, добавьте файлы чтобы проанализировать данные') 
        return render_template("main/index.html", page_title="Подгрузите файлы", flag=0)
    dates = table.index.values.astype('datetime64[D]').tolist()
    if allowed_dates.event_start.data <= allowed_dates.event_end.data:
        for date_index in dates:
            if date_index < allowed_dates.event_start.data or date_index > allowed_dates.event_end.data:
                date_index_str = date_index.strftime('%Y-%m-%d')
                table = table.drop(date_index_str)
        table_columns = table.columns.values.tolist()
        table_values = table.values.astype(float).tolist()
        dates = table.index.values.astype(str).tolist()
        table.plot(figsize=(10,10), subplots=True)
        plt.savefig(os.path.join('webapp/static/', 'my_plot.jpg'))
        table_columns.insert(0, "День")
        image_hidden = True
        for i in range(len(table_values)):
            table_values[i][:-1] = [round(elem) for elem in table_values[i][:-1]]
            table_values[i][-1] = format(table_values[i][-1], '.2f')
            table_values[i].insert(0, dates[i])
        return render_template("main/data_analysis.html", table_columns=table_columns, table_values=table_values, image_hidden=image_hidden)
    else:
        flash('Некорректно указан диапазон')
        return render_template("main/data_analysis.html") 


@blueprint.route('/add_files/<int:delete>', methods=['GET', 'POST'])
@user_required
def upload_file(delete=0):
    if delete == 1:
        current_user_id = current_user.get_id()
        try:
            delete_orders_data(current_user_id)
            flash('Записи в базе данных удалены')
        except ValueError:
            flash('У вас нет записей в базе данных') 
    flag = 0
    if request.method == 'POST':
        if 'file_1' not in request.files or 'file_2' not in request.files or 'file_3' not in request.files:
            flash('Недопустимый формат файла')
            return redirect(request.url)
        file_users = request.files['file_1']
        file_orders = request.files['file_2']
        file_expences = request.files['file_3']        
        if file_users.filename == '' and file_orders.filename == '' and file_expences.filename == '':
            flash('Файлы не добавлены')
            return redirect(request.url)
        flag = add_file(file_users, "fake_clients.csv", flag)
        flag = add_file(file_orders, "fake_orders.csv", flag)
        flag = add_file(file_expences, "fake_expences.csv", flag)    
    return render_template("main/index.html", page_title="Подгрузите файлы", flag=flag)