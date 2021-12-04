import time

from watchdog.observers import Observer

from roas_calculator.csv_handler import CsvHandler


def start_observer():
    csv_hander = CsvHandler()
    observer = Observer()
    observer.schedule(csv_hander, path='.', recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()


if __name__ == '__main__':
    start_observer()
