import pandas as pd
import matplotlib.pyplot as plt
from models import Order, Client
from db import engine
import pandas as pd
from db import db_session


def get_orders_data(current_user_id = 1):
    df_clients_id = pd.read_sql('''SELECT id FROM clients where user_id = {}'''.format(current_user_id), con=engine)
    df = pd.DataFrame({})
    client_id = []
    for i in range(len(df_clients_id)):
        client_id.append(df_clients_id.loc[i]['id'])
    client_id = ', '.join(str(id) for id in client_id)
    df = pd.read_sql('''SELECT * FROM orders where client_id IN ({})'''.format(client_id), con=engine)
    return df


def delete_orders_data(current_user_id = 1):
    for users_id in Client.query.filter(Client.user_id == current_user_id):
        Order.query.filter(Order.client_id == users_id.id).delete()
    Client.query.filter(Client.user_id == current_user_id).delete()
    db_session.commit()


def correct_data(df):
    df.columns = df.columns.str.lower()
    df['date_created'] = df['date_created'].astype('datetime64[ns]').dt.strftime('%Y/%m/%d')
    df.loc[df['earned'] != 0, 'Оплаты'] = 1 
    return df
    

def create_empty_df(df):    
    empty_df = pd.DataFrame()
    empty_df.index = pd.date_range(start=df['date_created'].min(), end=df['date_created'].max())
    empty_df.index = empty_df.index.strftime('%Y/%m/%d')
    empty_df.index.name = 'date_created'
    return empty_df


def merge_empty_df_with_results(df_corrected, empty_df):

    orders_by_day = df_corrected.groupby('date_created')['title'].size()
    sum_orders_by_day = df_corrected.groupby('date_created')['amount'].sum()
    payments_by_day = df_corrected[df_corrected['Оплаты'] == 1].groupby('date_created')['Оплаты'].size()
    sum_payments_by_day = df_corrected[df_corrected['Оплаты'] == 1].groupby('date_created')['earned'].sum()

    result_df = pd.concat([empty_df, orders_by_day], axis=1).groupby('date_created', as_index=True).sum()
    result_df = pd.concat([result_df, sum_orders_by_day], axis=1).groupby('date_created', as_index=True).sum()
    result_df = pd.concat([result_df, payments_by_day], axis=1).groupby('date_created', as_index=True).sum()
    result_df = pd.concat([result_df, sum_payments_by_day], axis=1).groupby('date_created', as_index=True).sum()

    result_df = result_df.rename(columns={'title': 'Заказов', 'amount': 'Сумма заказов, ₽', 'earned': 'Сумма оплат, ₽'})
    result_df.index = result_df.index.astype('datetime64[ns]')

    return result_df

def create_result_df():
    data = get_orders_data()
    corrected_data = correct_data(data)
    empty_df = create_empty_df(corrected_data)
    result_df = merge_empty_df_with_results(corrected_data, empty_df)
    return result_df
    
if __name__ == '__main__':
    #get_orders_data(1)
    delete_orders_data(2)