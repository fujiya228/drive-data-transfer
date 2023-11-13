import pandas as pd
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload, MediaIoBaseUpload
import io
from modules.google_api_client import create_drive_client
from modules.utils import convert_headers_to_data_row, check_encoding

# 参考：https://developers.google.com/resources/api-libraries/documentation/drive/v3/python/latest/drive_v3.files.html

drive_client = None

# init
def init_drive_client(service_account_file=None, scopes=None):
    global drive_client
    drive_client = create_drive_client(service_account_file, scopes)

# get
def get_file_info_list_from_drive(
        corpora=None,
        supportsAllDrives=True,
        includeItemsFromAllDrives=True,
        driveId=None,
        pageSize=50,
        q=None,
        fields='nextPageToken, files(id, name)'
    ):

    if drive_client is None:
        raise Exception('Please initialize drive client by calling init_drive_client() first.')

    print(f"search_query => {q}")

    results = drive_client.files().list(
        corpora=corpora,
        supportsAllDrives=supportsAllDrives,
        includeItemsFromAllDrives=includeItemsFromAllDrives,
        driveId=driveId,
        pageSize=pageSize,
        q=q,
        fields=fields
    ).execute()

    return results.get('files', []), results.get('nextPageToken', None)

def get_bytes_io_from_drive(file_id):
    if drive_client is None:
        raise Exception('Please initialize drive client by calling init_drive_client() first.')

    request = drive_client.files().get_media(fileId=file_id)

    io_file = io.BytesIO()
    downloader = MediaIoBaseDownload(io_file, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()

    return io_file

def get_df_from_drive(file_id, file_type, sheet_name=0, header=True):
    io_file = get_bytes_io_from_drive(file_id)
    io_file.seek(0) # BytesIOオブジェクトを返すときにすでにデータを読み終えた状態（つまりポインタが末尾にある状態）で返している可能性があるので、先頭に戻す

    if file_type == 'csv':
        io_file = check_encoding(io_file)
        df = pd.read_csv(io_file)
    elif file_type == 'json':
        df = pd.read_json(io_file)
    elif file_type == 'xlsx':
        df = pd.read_excel(io_file, sheet_name=sheet_name ,engine="openpyxl")
    else:
        raise Exception('Invalid file type.')

    if header:
        return df
    else:
        return convert_headers_to_data_row(df)

# create
def upload_file_to_drive(local_file_path, file_name, parent_folder_id, supportsAllDrives=None, supportsTeamDrives=None):
    if drive_client is None:
        raise Exception('Please initialize drive client by calling init_drive_client() first.')

    file_metadata = {
        'name': f'{file_name}',
        'parents': [parent_folder_id],
        'owners': ['me'],
    }

    media = MediaFileUpload(local_file_path)

    # 同じ名前のファイルが存在するかどうかを確認
    search_query = f"name='{file_name}' and parents in '{parent_folder_id}' and trashed = false"
    existing_files, _ = get_file_info_list_from_drive(q=search_query)

    print(f'Existing files: {existing_files}')
    if existing_files:
        # 同じ名前のファイルが存在する場合は更新する
        existing_file_id = existing_files[0]['id']
        result = update_file_in_drive(
            existing_file_id,
            local_file_path,
            supportsAllDrives,
            supportsTeamDrives
        )
    else:
        # 同じ名前のファイルが存在しない場合はアップロードする
        result = drive_client.files().create(
            body=file_metadata,
            media_body=media,
            supportsAllDrives=supportsAllDrives,
            supportsTeamDrives=supportsTeamDrives,
            fields='id'
        ).execute().get('id')

    return result

# update
def update_file_in_drive(file_id, file_source, supportsAllDrives=None, supportsTeamDrives=None):
    if drive_client is None:
        raise Exception('Please initialize drive client by calling init_drive_client() first.')

    # Check if file_source is a path (string type) or a MediaFileUpload object
    if isinstance(file_source, str):
        media = MediaFileUpload(file_source)
    elif isinstance(file_source, MediaFileUpload):
        media = file_source
    else:
        raise ValueError("file_source must be a file path (string) or MediaFileUpload object")

    result = drive_client.files().update(
        supportsTeamDrives=supportsTeamDrives,
        supportsAllDrives=supportsAllDrives,
        fileId=file_id,
        media_body=media,
        fields='id'
    ).execute()

    print(f'Existing files have been updated: {file_id}')

    return result.get('id')

def update_file_in_drive_from_df(file_id, df, supportsAllDrives=None, supportsTeamDrives=None):
    if drive_client is None:
        raise Exception('Please initialize drive client by calling init_drive_client() first.')

    # dfをcsvに変換してからアップロード
    media = MediaIoBaseUpload(
        io.BytesIO(df.to_csv(index=False).encode()),
        mimetype='text/csv',
        resumable=True
    )

    result = drive_client.files().update(
        supportsTeamDrives=supportsTeamDrives,
        supportsAllDrives=supportsAllDrives,
        fileId=file_id,
        media_body=media,
        fields='id'
    ).execute()

    print(f'Existing files have been updated: {file_id}')

    return result.get('id')

# delete
def trash_file_in_drive(file_id, supportsAllDrives=None, supportsTeamDrives=None):
    if drive_client is None:
        raise Exception('Please initialize drive client by calling init_drive_client() first.')

    result = drive_client.files().update(
        supportsTeamDrives=supportsTeamDrives,
        supportsAllDrives=supportsAllDrives,
        fileId=file_id,
        body={'trashed': True}
    ).execute()

    print(f'Existing files have been trashed: {file_id}')

    return result.get('id')

def delete_file_in_drive(file_id, supportsAllDrives=None, supportsTeamDrives=None):
    if drive_client is None:
        raise Exception('Please initialize drive client by calling init_drive_client() first.')

    drive_client.files().delete(
        supportsTeamDrives=supportsTeamDrives,
        supportsAllDrives=supportsAllDrives,
        fileId=file_id
    ).execute()

    print(f'Existing files have been deleted: {file_id}')
