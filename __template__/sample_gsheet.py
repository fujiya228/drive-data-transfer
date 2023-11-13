from modules.google_spreadsheet_client_wrapper import (
    init_spreadsheet_client,
    get_array_from_gsheet,
    get_df_from_gsheet
)

def main(event, context):
    init_spreadsheet_client('credentials/drive-service-credentials.json')

    gsheet_id = '1fgTYNvX2kCwiRABiiDFSvVJk1fGoBMiMcsk7-KkFhb8'
    worksheet_name = 'sheet_1'
    values = get_array_from_gsheet(gsheet_id, worksheet_name)

    print(values)

    df = get_df_from_gsheet(gsheet_id, worksheet_name)

    print(df)

if __name__ == '__main__':
    main(None, None)