from db import db_session
from models import User, Clients, Orders
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

import csv

def prepare_data(row):
    row['register_date'] = datetime.strptime(row['register_date'], '%Y-%m-%d')
    row['date_of_birth'] = datetime.strptime(row['date_of_birth'], '%Y-%m-%d')
    return row

def save_client(row):
    client = Clients(
        user_id=row['user_id'],
        email=row['email'],
        register_date=row['register_date'],
        firstname=row['firstname'],
        lastname=row['lastname'],
        phone_number=row['phone_number'],
        date_of_birth=row['date_of_birth']
    )
    db_session.add(client)
    try:
        db_session.commit()
    except SQLAlchemyError:
        db_session.rollback()
        raise

def process_row(row):
    row = prepare_data(row)
    save_client(row)

def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['user_id',  'email', 'register_date', 'firstname', 'lastname', 'phone_number',
                  'date_of_birth']
        reader = csv.DictReader(f, fields, delimiter=',')
        for row in reader:
            try:
                process_row(row)
            except (TypeError, ValueError) as e:
                print(f'При обработке возникла ошибка: {e}')
            except SQLAlchemyError as e:
                print(f'Ошибка целостности данных: {e}')

if __name__ == '__main__':
    read_csv('fake_users.csv')