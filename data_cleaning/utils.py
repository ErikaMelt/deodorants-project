from google.cloud import storage
from google.cloud.exceptions import Forbidden
from google.cloud.exceptions import NotFound
import pandas as pd
import datetime


def convert_file(df, col_name, data_type, date_format="%Y%m%d", col_names=None):
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
        The converted DataFrame.GIT S
    Raises
    ------
    ValueError
        If an invalid data type is provided.
        :type col_name: object
        :param data_type:
        :param df:
        :param col_name:
        :param col_names:
        :param date_format:
    """

    if data_type == 'str':
        df[col_name] = df[col_name].astype(str)
    elif data_type == 'date':
        df[col_name] = pd.to_datetime(df[col_name], format=date_format)
    elif data_type == 'int':
        df[col_name] = df[col_name].astype(int)
    elif data_type == 'str_m':
        if col_names is None:
            raise ValueError("When data_type is 'str_m', col_names must be provided.")
        df[col_names] = df[col_names].astype(str)
    else:
        raise ValueError("Invalid data_type. Valid options are 'str', 'date', and 'str_m'.")

    return df


def replace_regex(df: object, col_name: str, regex: str, value: str):
    """
    Find a regex pattern in the string and replace with the value passed.

    :param df: dataframe to replace regex
    :param col_name: column where the replacement will be done
    :param regex: pattern to find
    :param value: value to replace
    """
    df[col_name] = df[col_name].replace(to_replace=regex, value=value, regex=True)


def upload_to_bucket(bucket_name: str, file_path: str, blob_name: str) -> None:
    """
    Uploads a file to a Google Cloud Storage bucket.

    :param bucket_name: Name of the bucket to upload the file to.
    :param file_path: Path of the file to be uploaded.
    :param blob_name: Name of the blob to be created in the bucket.
    :raises google.cloud.exceptions.NotFound: If the specified bucket does not exist.
    :raises google.cloud.exceptions.Forbidden: If the user does not have permission to access the specified bucket.
    """
    try:
        # Create a client object with the specified credentials and get the bucket
        client = storage.Client.from_service_account_json('deodorants-7c413894015d.json')
        bucket = client.get_bucket(bucket_name)
    except (NotFound, Forbidden) as e:
        # Catch any exceptions that may occur while getting the bucket
        print(f"Error getting bucket {bucket_name}: {e}")
        return

    try:
        # Create a blob object and upload the file
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
    except Exception as e:
        # Catch any exceptions that may occur during the upload process
        print(f"Error uploading file {file_path} to bucket {bucket_name}/{blob_name}: {e}")
        return

    print(f"File {file_path} uploaded successfully to bucket {bucket_name}/{blob_name}")


def get_season(date):
    year = date.year
    seasons = [('invierno', datetime.date(year, 12, 21), datetime.date(year + 1, 3, 20)),
               ('primavera', datetime.date(year, 3, 21), datetime.date(year, 6, 20)),
               ('verano', datetime.date(year, 6, 21), datetime.date(year, 9, 20)),
               ('otono', datetime.date(year, 9, 21), datetime.date(year, 12, 20))]
    for season, start_date, end_date in seasons:
        if start_date <= pd.Timestamp(date) <= end_date:
            return season
    return 'invierno'


def remove_duplicates(s):
    seen = set()
    result = []
    for word in s.split():
        if word not in seen:
            result.append(word)
            seen.add(word)
    return " ".join(result)


