import io
import re

def convert_headers_to_data_row(df):
    # 列名を取得し、新しい行として追加
    df.loc[-1] = df.columns

    # 新しい行を先頭に移動
    df.index = df.index + 1
    df = df.sort_index()

    # 新しい列名を設定
    df.columns = range(df.shape[1])

    return df


def check_encoding(io_file):
    encoding_list = [
        'UTF-8',
        'UTF-16',
        'SHIFT_JIS',
        'CP932',
    ]
    bytes =  io_file.getvalue()
    for encoding in encoding_list:
        try:
            file_text = bytes.decode(encoding)
            print(f'encoding is "{encoding}"')
            break
        except UnicodeDecodeError as error:
            print(f'encoding is not "{encoding}"')

    io_file = io.StringIO(re.sub(r',\s*?\n', '\n', file_text))
    return io_file