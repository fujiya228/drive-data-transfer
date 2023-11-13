from modules.google_cloud_storage_client_wrapper import (
    init_cloudstorage_client,
    get_blob_list_from_gcs,
)

def main(event, context):
    # init clients
    # 
    # 以下の認証をサポートしている
    # - ①SAの認証ファイルを指定して、OAuth2.0の仕組みで認証（SAを複数に分けたい場合）
    # - ADC（アプリケーションのデフォルトの認証情報）を利用する
    #     - ②サービスアカウントの環境変数（SAを1つに固定で良い場合）
    #     - ③CLIで設定されたユーザー情報（ローカルのみ）
    #     - ④GCFのランタイム サービス アカウント（GCFのみ）
    # - モジュール読み込んだ時点ですでにADCで認証しておく
    # 
    # ※SA：Service Account
    # 
    # 1. SAの認証ファイルを指定する場合は、初期化メソッドにSAの認証ファイルを指定して初期化することができる
    # 2. 指定しない場合は、ADCで認証を試みる
    # 
    # 以下コメントアウトをはずして試してみてください

    # init_cloudstorage_client()
    # init_cloudstorage_client('credentials/gcs-service-credentials.json')

    blobs = get_blob_list_from_gcs('atarayo-test')

    for blob in blobs:
        print(blob.name)

if __name__ == '__main__':
    main(None, None)