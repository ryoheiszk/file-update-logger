import sys
import configparser
import os
import pandas as pd
from datetime import datetime

def load_settings(section, settings_file):
    config = configparser.ConfigParser()
    config.read(settings_file, encoding='utf-8')  # UTF-8エンコーディングを指定
    return config[section]

def create_excel_file(log_folder):
    # 現在の日付を取得して、ファイル名に使用する
    current_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")
    excel_file_name = f"event_log_{current_datetime}.xlsx"
    excel_file_path = os.path.join(log_folder, excel_file_name)
    return excel_file_path

def convert_log_to_excel(log_file_path, excel_file_path):
    data = []
    with open(log_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(' | ')
            if len(parts) == 3:
                # 日付と時刻を分割
                datetime_parts = parts[0].split()
                date = datetime_parts[0]
                time = datetime_parts[1]

                # 操作
                operation = parts[1]

                # ディレクトリとファイル名を分割
                directory_file_parts = parts[2].rsplit(' / ', 1)
                directory = directory_file_parts[0] + ' /'
                file_name = directory_file_parts[1] if len(directory_file_parts) > 1 else ""

                # 分割したデータをリストに追加
                data.append([date, time, operation, directory, file_name])

    # DataFrameを作成
    df = pd.DataFrame(data, columns=['日付', '時刻', '操作', 'ディレクトリ', 'ファイル'])

    # ExcelWriterを使用してDataFrameを書き込む
    with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Log')

        # ワークシートを取得
        worksheet = writer.sheets['Log']

        # 列幅を設定
        worksheet.set_column('A:A', 15)  # 日付
        worksheet.set_column('B:B', 10)  # 時刻
        worksheet.set_column('C:C', 5)  # 操作
        worksheet.set_column('D:D', 50)  # ディレクトリ
        worksheet.set_column('E:E', 30)  # ファイル

    print("Excelファイルに変換しました。")



def delete_log_file(log_file_path):
    # ログファイルを削除する
    os.remove(log_file_path)

if __name__ == "__main__":
    settings = load_settings("Settings", "src/settings.ini")
    log_folder = settings['log_folder']
    log_file_path = settings['log_file']

    # ログファイルの存在を確認
    if not os.path.exists(log_file_path):
        print("ログファイルが見つかりません。")
        sys.exit()

    # Excelファイルのパスを生成
    excel_file_path = create_excel_file(log_folder)

    convert_log_to_excel(log_file_path, excel_file_path)
    print("ログファイルの変換に成功しました。")

    delete_log_file(log_file_path)
    print("ログファイルを削除しました。")
