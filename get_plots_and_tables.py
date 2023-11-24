import pandas as pd
from get_orders_table import create_result_df
from get_expenses_table import get_expenses_table

def get_period():
    period = str(input('Введите разбивку для результирующей таблицы (Y-год, M-месяц, D-день)'))
    return period


def add_columns(df):
    df['Средний чек, ₽'] = df['Сумма оплат, ₽'] / df['Оплаты']
    df['Средний чек, ₽'] = df['Средний чек, ₽'].astype('int64')  
    df['Сумма оплат, ₽'] = df['Сумма оплат, ₽'].astype('int64')
    df['Конверсия в оплату, %'] = (df['Оплаты'] / df['Заказов']) * 100
    return df


def merge_orders_with_expenses(df1, df2):
    df1.index=df1.index.astype('datetime64[ns]')
    df2.index=df2.index.astype('datetime64[ns]')
    result = pd.merge(df1, df2, left_index=True, right_index=True)
    return result


def correct_collumns(df):
    df['spend'] = df['spend'].astype('int64')
    df = df.drop('user_id', axis=1)
    return df


def get_analysed_data(period, current_user_id):
    df_orders = create_result_df(current_user_id)
    df_expenses = get_expenses_table(current_user_id)
    #period = get_period()
    df = merge_orders_with_expenses(df_orders, df_expenses)
    df = correct_collumns(df)
    df = df.groupby(df.index.to_period(period)).sum()
    df = add_columns(df)
    return df


if __name__ == '__main__':
    df = get_analysed_data()

    print(df)
    print(df.plot(figsize=(15,25), subplots=True))