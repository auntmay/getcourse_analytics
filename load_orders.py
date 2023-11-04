from db import db_session
from models import User, Client, Order
from datetime import datetime
from normalise_orders_data import normalise_orders_data
from sqlalchemy.exc import SQLAlchemyError
from functools import lru_cache
import time
import csv


def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['email', 'date_created', 'date_closed',
        'title', 'status', 'amount',
        'tax', 'earned', 'currency', 'manager',
        'partner_id', 'utm_source', 'utm_medium', 'utm_campaign',
        'utm_content', 'utm_term', 'tags']
        reader = csv.DictReader(f, fields, delimiter=',')
        orders_data = []
        for row_num, row in enumerate(reader, start=1):
            try:
                prepare_data(row)
                orders_data.append(row)
            except (ValueError, TypeError) as e:
                save_dataformat_errors(row_num, row, 'Неправильный формат данных: {}', e)
        return orders_data


def prepare_data(row):
    row['date_created'] = datetime.strptime(row['date_created'], '%Y-%m-%d')
    row['date_closed'] = datetime.strptime(row['date_closed'], '%Y-%m-%d')
    row['tax'] = float(row['tax'])
    row['earned'] = float(row['earned'])
    return row


def save_dataformat_errors(row_num, row, error_text, exception):
    print("*" * 100)
    print(f'Ошибка в строке #{row_num}')
    print(error_text.format(exception))
    print("*" * 100)
    with open('orders_values_errors.csv', 'a', encoding='utf-8') as f:
        f.write(f'Ошибка в строке #{row_num}: {row}\nТекст ошибки: {error_text.format(exception)} \n\n')


def save_load_errors(num_rows, email):
    with open('orders_loading_errors.csv', 'a', encoding='utf-8') as f:
        f.write(f'Ошибка в строке #{num_rows}. Пользователя с адресом эл. почты {email} не существует в базе.\n', )


@lru_cache
def check_if_client_exist(email, num_rows, current_user_id = 1):
    try:
        client_id = Client.query.filter(Client.email == email, Client.user_id == current_user_id).first().id
        return client_id
    except AttributeError:
        print(f'В строке №{num_rows} возникла ошибка. Не существует пользователя с эл. почтой {email}, которому принадлежит заказ')
        save_load_errors(num_rows, email)
        return False


def save_orders(prepared_orders_data, current_user_id = 1):
    orders_list = []
    for num_rows, row in enumerate(prepared_orders_data, start=1):
        if check_if_client_exist(row['email'], num_rows, current_user_id):
            order = {'email':row['email'], 'client_id': check_if_client_exist(row['email'], num_rows, current_user_id), 'date_created':row['date_created'],
                'date_closed':row['date_closed'], 'title':row['title'], 'status':row['status'],
                'amount':row['amount'], 'tax':row['tax'], 'earned':row['earned'],
                'currency':row['currency'], 'manager':row['manager'], 'partner_id':row['partner_id'],
                'utm_source':row['utm_source'], 'utm_medium':row['utm_medium'], 'utm_campaign':row['utm_campaign'],
                'utm_content':row['utm_content'], 'utm_term':row['utm_term'], 'tags':row['tags']}
            orders_list.append(order) 
        #print(num_rows)
    try:
        db_session.bulk_insert_mappings(Order, orders_list)
        db_session.commit()
    except SQLAlchemyError as e:
        print(f'При загрузке данных возникла ошибка. Текст ошибки: {e}')
    except (ValueError, TypeError) as e:
        print(f'Ошибка типа данных. Текст ошибки: {e}')


if __name__ == '__main__':
    normalise_orders_data()
    orders_data = read_csv('normalised_orders.csv')
    save_orders(orders_data)