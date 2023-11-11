from datetime import timedelta
import os

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))     #Путь до текущей папки

SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(basedir, 'webapp2.db')        #Объединяет указаное имя с путем   
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = basedir
ALLOWED_EXTENSIONS = {'csv'}

SECRET_KEY = "ytvuebw2v7832932fuvh89298303-0009-00-007865%^%$^gjhbeuijcbweoi"

REMEMBER_COOKIE_DURATION = timedelta(days=5)
