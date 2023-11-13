import pandas as pd
from modules.google_api_client import create_spreadsheet_client

spreadsheet_client = None

# init
def init_spreadsheet_client(service_account_file=None, scopes=None):
    global spreadsheet_client
    spreadsheet_client = create_spreadsheet_client(service_account_file, scopes)

# get
def get_array_from_gsheet(gsheet_id, worksheet_name):
    if spreadsheet_client is None:
        raise Exception('Please initialize spreadsheet client by calling init_spreadsheet_client() first.')

    gsheet = spreadsheet_client.open_by_key(gsheet_id)
    worksheet = gsheet.worksheet(worksheet_name)
    values = worksheet.get_all_values()

    # delete newline code（BQで読み込めなくなるため整形）
    values = [[cell.replace('\n', '') for cell in row] for row in values]
    
    return values

def get_df_from_gsheet(gsheet_id, worksheet_name, header=True):
    values = get_array_from_gsheet(gsheet_id, worksheet_name)

    if header:
        return pd.DataFrame(values[1:], columns=values[0])
    else:
        return pd.DataFrame(values)

# update
def update_gsheet_from_df(gsheet_id, worksheet_name, df, header=True):
    if spreadsheet_client is None:
        raise Exception('Please initialize spreadsheet client by calling init_spreadsheet_client() first.')

    gsheet = spreadsheet_client.open_by_key(gsheet_id)
    worksheet = gsheet.worksheet(worksheet_name)

    # delete all values
    worksheet.clear()

    # update values
    if header:
        values = [df.columns.tolist()] + df.values.tolist()
    else:
        values = df.values.tolist()

    worksheet.update(values)

# append
def append_gsheet_from_df(gsheet_id, worksheet_name, df, header=True):
    if spreadsheet_client is None:
        raise Exception('Please initialize spreadsheet client by calling init_spreadsheet_client() first.')

    gsheet = spreadsheet_client.open_by_key(gsheet_id)
    worksheet = gsheet.worksheet(worksheet_name)

    # update values
    if header:
        values = [df.columns.tolist()] + df.values.tolist()
    else:
        values = df.values.tolist()

    worksheet.append_rows(values)