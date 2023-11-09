from db import db_session
from models import User, Expens
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
import csv


def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['user_id','date', 'spend', 'currency']
        reader = csv.DictReader(f, fields, delimiter=',')
        expenses_data = []
        for row in reader:
            prepare_data(row)
            expenses_data.append(row)
        return expenses_data


def prepare_data(row):
    row['date'] = datetime.strptime(row['date'], '%d.%m.%Y')
    row['user_id'] = int(row['user_id'])


def save_expenses(expenses_data):
    expens_list = []
    for row in expenses_data:
        expense = {'user_id': int(row['user_id']), 'date': row['date'],
                  'spend': row['spend'], 'currency': row['currency']}
        expens_list.append(expense)
    db_session.bulk_insert_mappings(Expens, expens_list, return_defaults=True)
    db_session.commit()


if __name__ == '__main__':
    data = read_csv('fake_expences.csv')
    save_expenses(data)
