import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_orders_data():
    file_name = str(input('Введите название файла с заказами: '))
    if file_name.endswith('.csv'):
        delim = str(input('Введите разделитель(по умолчанию ","): ')) or ','
        return pd.read_csv(f'{file_name}', delimiter=delim)
    elif file_name.endswith('.xlsx'):
        sheet = str(input('Введите название листа в таблице (по-умолчанию прочитается первый): ')) or 0
        return pd.read_excel(file_name, sheet_name=sheet, parse_dates=True)


def get_users_data():



def correct_data(df):
    df.columns = df.columns.str.lower()
    df['дата создания'] = df['дата создания'].astype('datetime64[ns]').dt.strftime('%Y/%m/%d')
    df.loc[df['заработано, rub'] != 0, 'Оплаты'] = 1 
    return df
    

def create_empty_df():    
    empty_df = pd.DataFrame()
    empty_df.index = pd.date_range(start=df['дата создания'].min(), end=df['дата создания'].max())
    empty_df.index = empty_df.index.strftime('%Y/%m/%d')
    empty_df.index.name = 'дата создания'
    return empty_df


def create_result_df(df_corrected, empty_df):

    users_data = get_users_data()

    orders_by_day = df_corrected.groupby('дата создания')['title'].size()
    sum_orders_by_day = df_corrected.groupby('дата создания')['стоимость, rub'].sum()
    payments_by_day = df_corrected[df_corrected['Оплаты'] == 1].groupby('дата создания')['Оплаты'].size()
    sum_payments_by_day = df_corrected[df_corrected['Оплаты'] == 1].groupby('дата создания')['заработано, rub'].sum()

    empty_df = pd.concat([empty_df, orders_by_day], axis=1).groupby('дата создания', as_index=True).sum()
    empty_df = pd.concat([empty_df, sum_orders_by_day], axis=1).groupby('дата создания', as_index=True).sum()
    empty_df = pd.concat([empty_df, payments_by_day], axis=1).groupby('дата создания', as_index=True).sum()
    empty_df = pd.concat([empty_df, sum_payments_by_day], axis=1).groupby('дата создания', as_index=True).sum()
    
    empty_df['Средний чек'] = empty_df['заработано, rub'] / empty_df['Оплаты']
    empty_df['Конверсия в оплату'] = empty_df['Оплаты'] / empty_df['title']

    empty_df = empty_df.rename(columns={'title': 'Заказов', 'стоимость, rub': 'Сумма заказов', 'заработано, rub': 'Сумма оплат'}) 

    return empty_df


if __name__ == "__main__":
    df = get_orders_data()
    df_corrected = correct_data(df)
    empty_df = create_empty_df()
    result = create_result_df(df_corrected, empty_df)

print(result)
    