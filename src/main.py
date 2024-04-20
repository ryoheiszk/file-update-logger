import configparser
from datetime import datetime
import time
import os
import re
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


def load_settings(target):
    config = configparser.ConfigParser()
    config.read('src/settings.ini', encoding='utf-8')
    return config['Settings'][target]


def load_exclude_patterns():
    patterns = []
    with open("src/exclude_patterns.txt", "r",  encoding='utf-8') as file:
        patterns = [line.strip() for line in file if line.strip()]
    return patterns


class LoggingEventHandler2(LoggingEventHandler):
    def __init__(self, exclude_patterns, debounce_time):
        super().__init__()
        self.exclude_patterns = exclude_patterns
        self.debounce_time = debounce_time
        self.last_event_time = 0
        self.last_event_path = ""

    def should_exclude(self, path):
        if not os.path.splitext(path)[1]:  # 拡張子がない場合は除外
            return True
        return any(re.search(pattern, path) for pattern in self.exclude_patterns)

    def should_debounce(self, event):
        current_time = time.time()
        if (self.last_event_path == event.src_path and
                (current_time - self.last_event_time) <= self.debounce_time):
            return True
        self.last_event_time = current_time
        self.last_event_path = event.src_path
        return False

    def get_timestamp(self):
        return datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    def on_created(self, event):
        if not self.should_exclude(event.src_path) and not self.should_debounce(event):
            timestamp = self.get_timestamp()
            message = f"{timestamp} | 作成 | {event.src_path}"
            self.write_log(message)

    def on_modified(self, event):
        if not self.should_exclude(event.src_path) and not self.should_debounce(event):
            timestamp = self.get_timestamp()
            message = f"{timestamp} | 更新 | {event.src_path}"
            self.write_log(message)

    def on_deleted(self, event):
        if not self.should_exclude(event.src_path) and not self.should_debounce(event):
            timestamp = self.get_timestamp()
            message = f"{timestamp} | 削除 | {event.src_path}"
            self.write_log(message)

    def write_log(self, message):
        # ログの分解
        datetime = message.split(" | ")[0]
        operation = message.split(" | ")[1]
        fullpath = message.split(" | ")[2]

        # 略式パスの取得
        base_directory = load_settings("base_directory") + "\\"
        simplified_path = fullpath.replace(base_directory, "")

        # 加工
        fullpath = fullpath.replace("\\", "/")
        simplified_path = simplified_path.replace("\\", " / ")

        # 再結合
        new_message = f"{datetime} | {operation} | {simplified_path} | {fullpath}"


        print(new_message)
        with open(LOG_FILE_PATH, "a",  encoding='utf-8') as log_file:
            log_file.write(new_message + "\n")

if __name__ == "__main__":
    DIRECTORY_TO_WATCH = load_settings("directory_to_watch")
    LOG_FILE_PATH = load_settings("log_folder") + "\\event_log.txt"
    exclude_patterns = load_exclude_patterns()
    event_handler = LoggingEventHandler2(exclude_patterns, debounce_time=1.0)
    observer = Observer()
    observer.schedule(event_handler, DIRECTORY_TO_WATCH, recursive=True)
    observer.start()
    print (f"「{DIRECTORY_TO_WATCH}」の監視を開始しました。")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
