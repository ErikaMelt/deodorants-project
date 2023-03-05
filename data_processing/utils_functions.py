import pandas as pd


def convert_file(df, col_name, data_type, col_names=None):
    """
    Convert a column in a DataFrame to a specified data type.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to be converted.
    col_name : str
        The name of the column to be converted.
    data_type : str
        The data type to convert the column to. Valid options are 'str', 'date', and 'str_m'.
    col_names : list of str, optional
        A list of column names to be converted. Only used when data_type is 'str_m'.

    Returns
    -------
    pandas.DataFrame
        The converted DataFrame.

    Raises
    ------
    ValueError
        If an invalid data type is provided.
    """

    if data_type == 'str':
        df[col_name] = df[col_name].astype(str)
    elif data_type == 'date':
        df[col_name] = pd.to_datetime(df[col_name], format='%Y%m%d', errors='coerce')
    elif data_type == 'str_m':
        if col_names is None:
            raise ValueError("When data_type is 'str_m', col_names must be provided.")
        df[col_names] = df[col_names].astype(str)
    else:
        raise ValueError("Invalid data_type. Valid options are 'str', 'date', and 'str_m'.")

    return df


def remove_non_ascii(df: object, col_name: str) -> object:
    """

    :param df:
    :param col_name:
    """
    df[col_name] = df[col_name].replace(to_replace=r'[^\x00-\x7F]+', value='', regex=True)


def replace_regex(df, col_name, regex, value):
    df[col_name] = df[col_name].replace(to_replace=regex, value=value, regex=True)


