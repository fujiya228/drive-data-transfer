from modules.google_cloud_storage_client_wrapper import (
    init_cloudstorage_client,
    upload_to_gcs_from_string,
)

from modules.google_drive_client_wrapper import (
    init_drive_client,
    get_df_from_drive,
)

def main(event, context):
    # init clients
    init_cloudstorage_client('credentials/gcs-service-credentials.json')
    init_drive_client('credentials/drive-service-credentials.json')

    # download
    df = get_df_from_drive('195AojbE2WjNMNGPrPzpfszWS3HTE0sxW', 'csv')

    # format data
    df['new_column'] = 'new_value'

    # upload
    upload_to_gcs_from_string('functions_test_bucket', 'main_sample.csv', df.to_csv(index=False))

if __name__ == '__main__':
    main(None, None)