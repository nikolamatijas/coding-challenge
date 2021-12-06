import logging

import daemon

from roas_calculator.csv_observer import CsvObserver


def run_daemon_process():
    csv_observer = CsvObserver()
    csv_observer.start_observer()


if __name__ == '__main__':
    with daemon.DaemonContext(working_directory='.'):
        logging.basicConfig(filename='logs.log', format='%(asctime)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.INFO)
        run_daemon_process()
