from modules.google_cloud_storage_client_wrapper import (
    init_cloudstorage_client,
    upload_to_gcs_from_string,
    upload_to_gcs_from_filename,
    get_blob_list_from_gcs,
    delete_blob_in_gcs,
    get_df_from_gcs,
)

def main(event, context):
    init_cloudstorage_client('credentials/gcs-service-credentials.json')

    bucket_name = 'functions_test_bucket'
    local_file_path = 'test_data/sample.csv'

    # upload_to_gcs_from_filename(bucket_name, file_name, local_file_path)
    upload_to_gcs_from_filename(bucket_name, 'sample.csv', local_file_path)

    # get_blob_list_from_gcs(bucket_name, prefix=None)
    blobs = get_blob_list_from_gcs(bucket_name)

    print(blobs)
    for blob in blobs:
        print(blob.name)

    # delete_blob_in_gcs(bucket_name, file_name)
    upload_to_gcs_from_filename(bucket_name, 'delete_target_sample.csv', local_file_path)
    delete_blob_in_gcs(bucket_name, 'delete_target_sample.csv')

    # get_df_from_gcs(bucket_name, file_name, file_type, sheet_name=0, header=True)
    df = get_df_from_gcs(bucket_name, 'sample.csv', 'csv')
    print(df)

    # upload_to_gcs_from_string(bucket_name, file_name, data)
    upload_to_gcs_from_string(bucket_name, 'from_string_sample.csv', df.to_csv(index=False))

if __name__ == '__main__':
    main(None, None)