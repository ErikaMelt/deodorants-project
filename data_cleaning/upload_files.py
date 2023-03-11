import pandas as pd
from google.cloud import storage
from google.cloud.exceptions import NotFound, Forbidden
from google.cloud import bigquery
from google.cloud.exceptions import NotFound, BadRequest
from google.oauth2.service_account import Credentials
import time
import pandas as pd


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
        The converted DataFrame.
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


def replace_regex(df: object, col_name: str, regex: str, value: str) -> object:
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


def get_data_big_query():
    try:
        key_path = 'deodorants-7c413894015d.json'
        credentials = Credentials.from_service_account_file(key_path)
        client = bigquery.Client(credentials=credentials)

        sql = """
        SELECT *
        FROM `deodorants.deodorants_trans.deodorants_merged` 
        ORDER BY fecha_trans DESC 
        """

        # Start the query job
        query_job = client.query(sql)

        while query_job.state != 'DONE':
            query_job.result()
            time.sleep(3)

        if query_job.state == 'DONE':
            # Read the data in chunks and concatenate the results
            df_list = []
            for i, row in enumerate(query_job.result(max_results=500000)):
                row_dict = dict(row.items())
                df_list.append(pd.DataFrame(row_dict, index=[i]))
                print(f'Reading chunk {len(df_list)}')
            df = pd.concat(df_list)
            return df
        else:
            print(query_job.result())

        return 'done'

    except NotFound as e:
        print(f'BigQuery table not found: {e}')
    except BadRequest as e:
        print(f'Invalid BigQuery request: {e}')
    except Exception as e:
        print(f'An error occurred while retrieving data from BigQuery: {e}')


def get_big_query_data(page_size=200000):
    try:
        key_path = 'deodorants-7c413894015d.json'
        credentials = Credentials.from_service_account_file(key_path)
        client = bigquery.Client(credentials=credentials)

        sql_template = """
        SELECT *
        FROM `deodorants.deodorants_trans.deodorants_merged` 
        ORDER BY fecha_trans, idb, id_producto
        LIMIT {page_size}
        OFFSET {offset}
        """

        # Start the first query job
        offset = 0
        query_job = client.query(sql_template.format(page_size=page_size, offset=offset))

        # Read the data in chunks and concatenate the results
        df_list = []
        while True:
            for i, row in enumerate(query_job.result()):
                row_dict = dict(row.items())
                df_list.append(pd.DataFrame(row_dict, index=[i]))
                print(f'Reading chunk {len(df_list)}')
            if query_job.next_page_token is None:
                break
            else:
                offset += page_size
                query_job = client.query(sql_template.format(page_size=page_size, offset=offset),
                                         job_config=bigquery.QueryJobConfig(
                                             use_query_cache=False,
                                             maximum_bytes_billed=10 * 1024 * 1024 * 1024
                                             # set the maximum bytes billed to 10GB
                                         ))

        df = pd.concat(df_list)
        return df

    except NotFound as e:
        print(f'BigQuery table not found: {e}')
    except BadRequest as e:
        print(f'Invalid BigQuery request: {e}')
    except Exception as e:
        print(f'An error occurred while retrieving data from BigQuery: {e}')



