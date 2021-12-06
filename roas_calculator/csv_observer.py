import time

from watchdog.observers import Observer

from roas_calculator.csv_handler import CsvHandler


class CsvObserver:
    """
    CsvObserver class represents observer thread that schedules watching directories and dispatches calls to
    event handlers for any new CSV file.

    Attributes:
        observer(watchdog.observers.Observer): Observer thread
    """
    def __init__(self):
        """
        The constructor for CsvObserver class.
        """
        self.observer = Observer()
        self.observer.schedule(event_handler=CsvHandler(), path='.', recursive=False)
        self.observer.daemon = True

    def start_observer(self):
        """Starts executing of observer."""
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            self.observer.join()
