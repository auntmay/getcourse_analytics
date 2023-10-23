import os
from flask import Blueprint, current_app, render_template, Flask, flash, request, redirect, url_for
from webapp.user.decorators import user_required
from werkzeug.utils import secure_filename
from webapp.config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER 

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
    return render_template("main/data_analysis.html")
    


@blueprint.route('/', methods=['GET', 'POST'])
@user_required
def upload_file():
    flag = 0
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file_1' not in request.files or 'file_2' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file_users = request.files['file_1']
        file_orders = request.files['file_2']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file_users.filename == '' and file_orders.filename == '':
            flash('Файлы не добавлены')
            return redirect(request.url)
        if file_users and allowed_file(file_users.filename):
            filename = "Users.csv"
            file_users.save(os.path.join(UPLOAD_FOLDER, filename))
            flag += 1
        if file_orders and allowed_file(file_orders.filename):
            filename = "Orders.csv"
            file_orders.save(os.path.join(UPLOAD_FOLDER, filename))
            flag += 1
    return render_template("main/index.html", page_title = "Подгрузите файлы", flag = flag)
