import logging
import time

import daemon
from watchdog.observers import Observer

from roas_calculator.csv_handler import CsvHandler


def run_daemon_process():
    """
    Initialize and start observer thread that schedules watching directories and dispatches calls to event handlers for
    any new CSV file.
    """
    observer = Observer()
    observer.schedule(event_handler=CsvHandler(), path='.', recursive=False)
    observer.daemon = True
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()


if __name__ == '__main__':
    with daemon.DaemonContext(working_directory='.'):
        logging.basicConfig(filename='logs.log', format='%(asctime)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.INFO)
        run_daemon_process()
