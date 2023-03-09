from google.cloud import bigquery
from google.cloud.exceptions import NotFound, BadRequest
from google.oauth2.service_account import Credentials
import time
import pandas as pd


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


df = get_big_query_data()

#%%
