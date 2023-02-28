import pandas as pd


def convert_file(df, col_name, data_type):
    if data_type == 'str':
        df[col_name] = df[col_name].astype(str)
        return df
    if data_type == 'date':
        df[col_name] = pd.to_datetime(df[col_name], format='%Y%m%d', errors='coerce')
        return df
