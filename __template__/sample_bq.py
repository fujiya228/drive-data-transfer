from modules.google_big_query_client_wrapper import (
    init_bigquery_client,
    get_df_from_bq
)

def main(event, context):
    init_bigquery_client('credentials/bq-service-credentials.json')

    query = 'SELECT * FROM `mp-cdp-production.source__honeycomb.result_conversion` LIMIT 10'
    df = get_df_from_bq(query)

    print(df)

if __name__ == '__main__':
    main(None, None)