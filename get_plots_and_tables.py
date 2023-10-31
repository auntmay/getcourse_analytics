from get_orders_sql import create_result_df


def get_period():
    period = str(input('Введите разбивку для результирующей таблицы (Y-год, M-месяц, D-день)'))
    return period


def add_columns(df):
    df['Средний чек, ₽'] = df['Сумма оплат, ₽'] / df['Оплаты']
    df['Средний чек, ₽'] = df['Средний чек, ₽'].astype('int64')  
    df['Сумма оплат, ₽'] = df['Сумма оплат, ₽'].astype('int64')
    df['Конверсия в оплату, %'] = (df['Оплаты'] / df['Заказов']) * 100
    return df


def get_analysed_data():
    df = create_result_df()
    period = get_period()
    df = df.groupby(df.index.to_period(period)).sum()
    df = add_columns(df)
    return df


if __name__ == '__main__':
    df = get_analysed_data()

    print(df)
    print(df.plot(figsize=(15,25), subplots=True))