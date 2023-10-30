from get_orders_sql import get_orders_data, correct_data, create_empty_df, create_result_df

def get_orders_dataframe():
    
    df = get_orders_data()
    df_corrected = correct_data(df)
    empty_df = create_empty_df(df)
    df_orders_result = create_result_df(df_corrected, empty_df)

    return df_orders_result


print(get_orders_dataframe())
print(get_orders_dataframe().plot(subplots=True, figsize=(15,25)))