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



