import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_dataframe():
    file_name = str(input('Введите название файла: '))
    if file_name.endswith('.csv'):
        delim = str(input('Введите разделитель(по умолчанию ","): ')) or ','
        return pd.read_csv(f'{file_name}', delimiter=delim)
    elif file_name.endswith('.xlsx'):
        sheet = str(input('Введите название листа в таблице (по-умолчанию прочитается первый): ')) or 0
        return pd.read_excel(file_name, sheet_name=sheet, parse_dates=True)
    
df = get_dataframe()