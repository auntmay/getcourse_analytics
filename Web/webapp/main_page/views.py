from flask import Blueprint, current_app, render_template

blueprint = Blueprint('main_page', __name__)

@blueprint.route('/')
def index():
    title = "Подгрузите файл"
    return render_template("main/index.html", page_title = title)