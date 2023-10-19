import pandas as pd


def get_data():
    delimiter = str(input('Введите разделитель (по-умолчанию разделитель -- ","): ')) or ','
    df = pd.read_csv(r'orders_raw.csv', delimiter=delimiter)
    return df


def delete_unnecessary_columns(df):

    df.columns = df.columns.str.lower()
    df = df[['id пользователя', 'дата создания', 'дата оплаты', 'title', 
            'статус', 'стоимость, rub', 'налог', 'заработано', 'валюта',
            'менеджер', 'id партнера', 'utm_source', 'utm_medium', 'utm_campaign',
            'utm_content', 'utm_term', 'теги']]
    return df


def rename_columns(df):

    df.rename(columns={
        'id пользователя': 'client_id',
        'дата создания': 'date_created',
        'дата оплаты': 'date_closed',
        'статус': 'status',
        'стоимость, rub': 'amount',
        'налог': 'tax',
        'заработано': 'earned',
        'валюта': 'currency',
        'менеджер': 'manager',
        'id партнера': 'partner_id',
        'теги': 'tags',
    }, inplace=True)
    return df


def correct_dates(df):

    df['date_created'] = df['date_created'].astype('datetime64[ns]').dt.strftime('%Y-%m-%d')
    df['date_closed'] = df['date_closed'].astype('datetime64[ns]').dt.strftime('%Y-%m-%d')
    return df


def to_result_csv(df):
    df.to_csv(r'raw_to_normal_data/result.csv', index=False)


def correct_data():

    df = get_data()
    df = delete_unnecessary_columns(df)
    df = rename_columns(df)
    df = correct_dates(df)
    to_result_csv(df)


if __name__ == '__main__':
    correct_data()
