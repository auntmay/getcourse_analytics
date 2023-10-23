from db import db_session
from models import User, Clients, Orders
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from normalise_users_data import normalise_users_data
import csv


def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['user_id',  'email', 'register_date', 'firstname', 'lastname', 'phone_number',
                  'date_of_birth']
        reader = csv.DictReader(f, fields, delimiter=',')
        clients_data = []
        for row_num, row in enumerate(reader, start=1):
            try:
                prepare_data(row)
                clients_data.append(row)
            except (ValueError, TypeError) as e:
                save_error(row_num, row, 'Неправильный формат данных: {}', e)
        return clients_data


def prepare_data(row):
    row['register_date'] = datetime.strptime(row['register_date'], '%Y-%m-%d')
    row['date_of_birth'] = datetime.strptime(row['date_of_birth'], '%Y-%m-%d')
    return row


def save_error(row_num, row, error_text, exception):
    print("*" * 100)
    print(f'Ошибка в строке #{row_num}')
    print(error_text.format(exception))
    print("*" * 100)
    with open('clients_errors.csv', 'a', encoding='utf-8') as f:
        f.write(f'Ошибка в строке #{row_num}: {row}\nТекст ошибки: {error_text.format(exception)} \n\n')


def save_clients(prepared_clients_data):
    clients_list = []
    for row in prepared_clients_data:
        client = {'user_id': row['user_id'], 'email':row['email'],
                'register_date':row['register_date'], 'firstname':row['firstname'],
                'lastname':row['lastname'], 'phone_number':row['phone_number'],
                 'date_of_birth':row['date_of_birth']}
        clients_list.append(client)
    try:
        db_session.bulk_insert_mappings(Clients, clients_list, return_defaults=True)
        db_session.commit()
    except SQLAlchemyError as e:
        print(f'При загрузке данных возникла ошибка: {e}')
    except (ValueError, TypeError) as e:
        print(f'Ошибка типа данных: {e}')

if __name__ == '__main__':
    # normalise_users_data()
    clients_data = read_csv('normalised_clients.csv')
    save_clients(clients_data)