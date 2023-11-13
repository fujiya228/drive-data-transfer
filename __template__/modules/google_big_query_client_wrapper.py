from modules.google_api_client import create_bigquery_client
from modules.utils import convert_headers_to_data_row

# 参考：https://cloud.google.com/python/docs/reference/bigquery/latest

bigquery_client = None

# init
def init_bigquery_client(service_account_file=None):
    global bigquery_client
    bigquery_client = create_bigquery_client(service_account_file)

# get
def get_df_from_bq(query, header=True):
    if bigquery_client is None:
        raise Exception('Please initialize bigquery client by calling init_bigquery_client() first.')

    df = bigquery_client.query(query).to_dataframe()

    if header:
        return df
    else:
        return convert_headers_to_data_row(df)
