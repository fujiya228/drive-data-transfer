import pandas as pd
from modules.google_api_client import create_cloudstorage_client
from modules.utils import convert_headers_to_data_row, check_encoding
import io

# 参考：https://cloud.google.com/python/docs/reference/storage/latest

cloudstorage_client = None
_buckets_cache = {}

# init
def init_cloudstorage_client(service_account_file=None):
    global cloudstorage_client
    cloudstorage_client = create_cloudstorage_client(service_account_file)

# get
def get_bucket(bucket_name):
    if cloudstorage_client is None:
        raise Exception('Please initialize cloudstorage client by calling init_cloudstorage_client() first.')

    if bucket_name not in _buckets_cache:
        _buckets_cache[bucket_name] = cloudstorage_client.get_bucket(bucket_name)
    return _buckets_cache[bucket_name]

def get_blob(bucket_name, file_name):
    bucket = get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    return blob

def get_blob_list_from_gcs(bucket_name, prefix=None):
    bucket = get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)
    return blobs

def get_bytes_io_from_gcs(bucket_name, file_name):
    blob = get_blob(bucket_name, file_name)
    content = blob.download_as_string()
    return io.BytesIO(content)

def get_df_from_gcs(bucket_name, file_name, file_type, sheet_name=0, header=True):
    io_file = get_bytes_io_from_gcs(bucket_name, file_name)
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

def download_from_gcs(bucket_name, file_name, local_file_path):
    blob = get_blob(bucket_name, file_name)
    blob.download_to_filename(local_file_path)
    print(f'File {file_name} has been downloaded to {local_file_path}')

# create
def upload_to_gcs_from_string(bucket_name, file_name, data):
    blob = get_blob(bucket_name, file_name)
    blob.upload_from_string(data=data)
    print(f'File {file_name} has been uploaded to {bucket_name}/{file_name}')

def upload_to_gcs_from_filename(bucket_name, file_name, local_file_path):
    blob = get_blob(bucket_name, file_name)
    blob.upload_from_filename(local_file_path)
    print(f'File {local_file_path} has been uploaded to {bucket_name}/{file_name}')

# delete
def delete_blob_in_gcs(bucket_name, file_name):
    blob = get_blob(bucket_name, file_name)
    blob.delete()
    print(f'File {file_name} has been deleted from {bucket_name}')
