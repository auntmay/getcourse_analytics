import pandas as pd
import matplotlib.pyplot as plt
from models import Order, Client
from db import engine
import pandas as pd
import matplotlib.pyplot as plt


def get_expenses_sql(current_user_id=1):
    df = pd.read_sql('''SELECT user_id, date, spend, currency FROM expenses where user_id IN ({})'''.format(current_user_id), con=engine)
    return df


def correct_data(df):
    df = df.rename(columns={'date':'date_created'})
    df.set_index(['date_created'], drop=True, inplace=True)
    df = df.drop(columns=['currency'])
    return df


def get_expenses_table(current_user_id=1):
    data = get_expenses_sql(current_user_id)
    result = correct_data(data)
    return result
