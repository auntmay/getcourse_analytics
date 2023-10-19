from db import db_session
from models import User, Clients, Orders
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

import csv

def prepare_data(row):
    row['date_created'] = datetime.strptime(row['date_created'], '%Y-%m-%d')
    row['date_closed'] = datetime.strptime(row['date_closed'], '%Y-%m-%d')
    row['tax'] = float(row['tax'])
    row['earned'] = float(row['earned'])
    return row

def save_client(row):
    order = Orders(
        client_id=row['client_id'],
        date_created=row['date_created'],
        date_closed=row['date_closed'],
        title=row['title'],
        status=row['status'],
        amount=row['amount'],
        tax=row['tax'],
        earned=row['earned'],
        currency=row['currency'],
        manager=row['manager'],
        partner_id=row['partner_id'],
        utm_source=row['utm_source'],
        utm_medium=row['utm_medium'],
        utm_campaign=row['utm_campaign'],
        utm_content=row['utm_content'],
        utm_term=row['utm_term'],
        tags=row['tags']
    )
    db_session.add(order)
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
        fields = ['client_id', 'date_created', 'date_closed',
        'title', 'status', 'amount',
        'tax', 'earned', 'currency', 'manager',
        'partner_id', 'utm_source', 'utm_medium', 'utm_campaign',
        'utm_content', 'utm_term', 'tags']
        reader = csv.DictReader(f, fields, delimiter=',')
        for row in reader:
            try:
                process_row(row)
            except (TypeError, ValueError) as e:
                print(f'При обработке возникла ошибка: {e}')
            except SQLAlchemyError as e:
                print(f'Ошибка целостности данных: {e}')

if __name__ == '__main__':
    read_csv('fake_orders.csv')