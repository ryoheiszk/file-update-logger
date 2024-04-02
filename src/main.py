import configparser
from datetime import datetime
import time
import os
import re
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


def load_settings(target):
    config = configparser.ConfigParser()
    config.read('src/settings.ini')
    return config['Settings'][target]


def load_exclude_patterns():
    patterns = []
    with open("src/exclude_patterns.txt", "r") as file:
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
        filename = os.path.basename(path)
        if not os.path.splitext(filename)[1]:  # 拡張子がない場合は除外
            return True
        return any(re.search(pattern, filename) for pattern in self.exclude_patterns)

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

    def abbreviate_path(full_path, base_path):
        if full_path.startswith(base_path):
            return "..." + full_path[len(base_path):]
        return full_path

    def write_log(self, message):
        # メッセージの加工: 一致する部分を非表示
        base_directory = load_settings("base_directory")
        message = message.replace(base_directory, "")

        # メッセージの加工: 置き換え
        message = message.replace("\\", " / ")

        print(message)
        with open(LOG_FILE_PATH, "a") as log_file:
            log_file.write(message + "\n")

if __name__ == "__main__":
    DIRECTORY_TO_WATCH = load_settings("directory_to_watch")
    LOG_FILE_PATH = load_settings("log_file")
    exclude_patterns = load_exclude_patterns()
    event_handler = LoggingEventHandler2(exclude_patterns, debounce_time=1.0)
    observer = Observer()
    observer.schedule(event_handler, DIRECTORY_TO_WATCH, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()