from modules.google_drive_client_wrapper import (
    init_drive_client,
    get_df_from_drive,
    get_file_info_list_from_drive,
    update_file_in_drive,
    update_file_in_drive_from_df,
    upload_file_to_drive,
    trash_file_in_drive,
    delete_file_in_drive,
)
import pandas as pd

def main(event, context):
    init_drive_client('credentials/drive-service-credentials.json')

    # get_df_from_drive(file_id, file_type='csv', sheet_name=0, header=True)

    # csv
    file_id = '195AojbE2WjNMNGPrPzpfszWS3HTE0sxW'
    df = get_df_from_drive(file_id, file_type='csv')
    df.to_csv('test_data/output.csv', index=False)
    print(df)

    # json
    file_id = '1f6x5u_Zsitdbqr77xsoa0ZileWdy1Qdw'
    df = get_df_from_drive(file_id, file_type='json')
    print(df)

    # xlsx
    file_id = '1qyOLP3F97bmncwgnLr-dyrVC7oTG1D0u'
    df = get_df_from_drive(file_id, file_type='xlsx', sheet_name=1)
    print(df)

    # get_file_info_list_from_drive(
    #     corpora=None,
    #     supportsAllDrives=True,
    #     includeItemsFromAllDrives=True,
    #     pageSize=50,
    #     q=None,
    #     fields='nextPageToken, files(id, name)'
    # )

    file_info_list, nextPageToken = get_file_info_list_from_drive(q="parents in '1EqZGAidKX0NjXONEOkCGTqcM_jcO1f4h' and trashed = false")

    print(f'file_info_list: {file_info_list}')
    print(f'nextPageToken: {nextPageToken}')

    # update_file_in_drive(file_id, file_source, supportsTeamDrives=True, supportsAllDrives=True)
    result = update_file_in_drive('195AojbE2WjNMNGPrPzpfszWS3HTE0sxW', 'test_data/output.csv')
    print(f'result: {result}')

    # update_file_in_drive_from_df(file_id, df, file_type='csv', supportsTeamDrives=True, supportsAllDrives=True)
    df = pd.read_csv('test_data/output.csv')
    result = update_file_in_drive_from_df('195AojbE2WjNMNGPrPzpfszWS3HTE0sxW', df)
    print(f'result: {result}')

    # upload_file_to_drive(local_file_path, file_name, parent_folder_id, supportsAllDrives=None, supportsTeamDrives=None)
    result = upload_file_to_drive('test_data/output.csv', 'new_output.csv', '1EqZGAidKX0NjXONEOkCGTqcM_jcO1f4h')
    print(f'result: {result}')

    # trash_file_in_drive(file_id, supportsTeamDrives=None, supportsAllDrives=None)
    result = trash_file_in_drive(result)
    print(f'result: {result}')

    # delete_file_in_drive(file_id, supportsTeamDrives=None, supportsAllDrives=None)
    delete_file_in_drive(result)

if __name__ == '__main__':
    main(None, None)