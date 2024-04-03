import configparser
import os
from datetime import datetime
import pandas as pd

def load_settings(settings_file):
    config = configparser.ConfigParser()
    config.read(settings_file)
    return config['Settings']

def create_excel_file(log_file_dir):
    # 現在の日付を取得して、ファイル名に使用する
    current_date = datetime.now().strftime("%Y%m%d")
    excel_file_name = f"event_log_{current_date}.xlsx"
    excel_file_path = os.path.join(log_file_dir, excel_file_name)
    return excel_file_path

def convert_log_to_excel(log_file_path, excel_file_path):
    # ログファイルをDataFrameに読み込む
    df = pd.read_csv(log_file_path, header=None, names=['Log'])

    # Excelファイルに書き込む
    df.to_excel(excel_file_path, index=False)

    print("Excelファイルに変換しました。")

def delete_log_file(log_file_path):
    # ログファイルを削除する
    os.remove(log_file_path)
    print("ログファイルを削除しました。")

if __name__ == "__main__":
    settings = load_settings("src/settings.ini")
    log_file_dir = settings['base_directory']
    log_file_path = settings['log_file']

    # Excelファイルのパスを生成
    excel_file_path = create_excel_file(log_file_dir)

    # ログファイルをExcel形式に変換
    convert_log_to_excel(log_file_path, excel_file_path)

    # ログファイルを削除
    # delete_log_file(log_file_path)
