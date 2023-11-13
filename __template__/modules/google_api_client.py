from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from google.cloud import bigquery
from google.cloud import storage
from google.auth import default
import gspread

DEFAULT_DRIVE_SCOPES = [
    'https://www.googleapis.com/auth/drive',
]
DEFAULT_GSHEET_SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]

def _get_credentials_type(credentials):
    if hasattr(credentials, 'service_account_email'):
        return "Service Account by Environment Variable"
    elif hasattr(credentials, 'refresh_token'):
        return "Authorized User"
    else:
        return "GCF Runtime Service Account"

def _get_credentials(service_account_file, scopes):
    try:
        if service_account_file:
            print(f"Using service account file from args: {service_account_file}")
            print()
            return Credentials.from_service_account_file(service_account_file, scopes=scopes)

        credentials, _ = default(scopes=scopes)
        print(f"Using default credentials type: {_get_credentials_type(credentials)}")
        print("types are:")
        print("- Service Account by Environment Variable")
        print("- Authorized User")
        print("- GCF Runtime Service Account")
        print()
        return credentials
    except Exception as e:
        print(f"An error occurred while getting credentials: {e}")
        print()
        return None

def create_drive_client(service_account_file, scopes=None):
    scopes = scopes or DEFAULT_DRIVE_SCOPES
    credentials = _get_credentials(service_account_file, scopes)
    return build('drive', 'v3', credentials=credentials) if credentials else None

def create_bigquery_client(service_account_file):
    credentials = _get_credentials(service_account_file, None)
    return bigquery.Client(credentials=credentials) if credentials else None

def create_cloudstorage_client(service_account_file):
    credentials = _get_credentials(service_account_file, None)
    return storage.Client(credentials=credentials) if credentials else None

def create_spreadsheet_client(service_account_file, scopes=None):
    scopes = scopes or DEFAULT_GSHEET_SCOPES
    credentials = _get_credentials(service_account_file, scopes)
    return gspread.authorize(credentials) if credentials else None
