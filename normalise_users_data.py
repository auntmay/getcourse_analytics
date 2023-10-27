import pandas as pd


def get_data():
    df = pd.read_csv(r'fake_clients.csv', delimiter=',')
    return df


def delete_unnecessary_columns(df):

    df.columns = df.columns.str.lower()
    df = df[['email', 'создан',  'имя',  'фамилия',  'телефон',
             'дата рождения']]
    
    df['user_id'] = 5
    new_cols = ['user_id', 'email', 'создан',  'имя',  'фамилия',  'телефон',
             'дата рождения']
    df = df[new_cols]
    
    return df


def rename_columns(df):

    df.rename(columns={
        'создан': 'register_date',
        'имя': 'firstname',
        'фамилия': 'lastname',
        'телефон': 'phone_number',
        'дата рождения': 'date_of_birth'
    }, inplace=True)
    return df


def correct_dates(df):

    df['register_date'] = df['register_date'].astype('datetime64[ns]').dt.strftime('%Y-%m-%d')
    df['date_of_birth'] = df['date_of_birth'].astype('datetime64[ns]').dt.strftime('%Y-%m-%d')
    return df


def to_result_csv(df):
    df.to_csv(r'normalised_clients.csv', index=False, header=False)


def normalise_users_data():

    df = get_data()
    df = delete_unnecessary_columns(df)
    df = rename_columns(df)
    df = correct_dates(df)
    to_result_csv(df)

if __name__ == '__main__':
    normalise_users_data()


