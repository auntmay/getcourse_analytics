import pandas as pd
import matplotlib.pyplot as plt
from models import Order, Client
from db import engine

import pandas as pd
import matplotlib.pyplot as plt


def get_orders_data():
    df = pd.read_sql('orders', con=engine)
    return df


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


def create_result_df(df_corrected, empty_df):

    orders_by_day = df_corrected.groupby('date_created')['title'].size()
    sum_orders_by_day = df_corrected.groupby('date_created')['amount'].sum()
    payments_by_day = df_corrected[df_corrected['Оплаты'] == 1].groupby('date_created')['Оплаты'].size()
    sum_payments_by_day = df_corrected[df_corrected['Оплаты'] == 1].groupby('date_created')['earned'].sum()

    empty_df = pd.concat([empty_df, orders_by_day], axis=1).groupby('date_created', as_index=True).sum()
    empty_df = pd.concat([empty_df, sum_orders_by_day], axis=1).groupby('date_created', as_index=True).sum()
    empty_df = pd.concat([empty_df, payments_by_day], axis=1).groupby('date_created', as_index=True).sum()
    empty_df = pd.concat([empty_df, sum_payments_by_day], axis=1).groupby('date_created', as_index=True).sum()

    empty_df = empty_df.rename(columns={'title': 'Заказов', 'amount': 'Сумма заказов, ₽', 'earned': 'Сумма оплат, ₽'})
    
    empty_df['Средний чек, ₽'] = empty_df['Сумма оплат, ₽'] / empty_df['Оплаты']
    empty_df['Средний чек, ₽'] = empty_df['Средний чек, ₽'].astype('int64')  
    empty_df['Сумма оплат, ₽'] = empty_df['Сумма оплат, ₽'].astype('int64')
    empty_df['Конверсия в оплату, %'] = (empty_df['Оплаты'] / empty_df['Заказов']) * 100

    return empty_df
    
    