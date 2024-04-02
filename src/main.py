import configparser
import time
import os
import re
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

# 設定ファイルから設定を読み込む関数
def load_settings(target):
    config = configparser.ConfigParser()
    config.read('src/settings.ini')
    return config['Settings'][target]


# 監視対象のディレクトリとログファイルのパス、除外パターンファイルのパスを定数で設定
DIRECTORY_TO_WATCH = load_settings("directory_to_watch")  # 監視したいディレクトリのパスに変更
LOG_FILE_PATH = load_settings("log_file")
EXCLUDE_PATTERN_FILE = "src/exclude_patterns.txt"  # 除外パターンを記述したファイルのパス


# 除外パターンを読み込む
def load_exclude_patterns():
    patterns = []
    with open(EXCLUDE_PATTERN_FILE, "r") as file:
        patterns = [line.strip() for line in file if line.strip()]
    return patterns


# LoggingEventHandlerを上書きして動作を変更
class LoggingEventHandler2(LoggingEventHandler):
    def __init__(self, exclude_patterns):
        super().__init__()  # 親クラスのコンストラクタを呼び出し
        self.exclude_patterns = exclude_patterns

    def write_log(self, message):
        with open(LOG_FILE_PATH, "a") as log_file:
            log_file.write(message + "\n")

    def should_exclude(self, path):
        filename = os.path.basename(path)  # ファイル名のみを取得
        # 拡張子がない場合はTrueを返して除外
        if not os.path.splitext(filename)[1]:
            return True
        return any(re.search(pattern, filename) for pattern in self.exclude_patterns)

    def on_created(self, event):
        if not self.should_exclude(event.src_path):
            message = "生成されました: " + event.src_path
            print(message)
            self.write_log(message)

    def on_modified(self, event):
        if not self.should_exclude(event.src_path):
            message = "修正されました: " + event.src_path
            print(message)
            self.write_log(message)

    def on_deleted(self, event):
        if not self.should_exclude(event.src_path):
            message = "削除されました: " + event.src_path
            print(message)
            self.write_log(message)

if __name__ == "__main__":
    exclude_patterns = load_exclude_patterns()
    event_handler = LoggingEventHandler2(exclude_patterns)
    observer = Observer()
    observer.schedule(event_handler, DIRECTORY_TO_WATCH, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
