import os
import time

from watchdog.events import PatternMatchingEventHandler

from roas_calculator.roas_calculator import RoasCalculator


class CsvHandler(PatternMatchingEventHandler):
    def __init__(self):
        PatternMatchingEventHandler.__init__(self, patterns=['*.csv'],
                                             ignore_directories=True, case_sensitive=False)

    def on_created(self, event):
        init_size = -1
        while True:
            current_size = os.path.getsize(event.src_path)
            if current_size == init_size:
                break
            else:
                init_size = os.path.getsize(event.src_path)
                time.sleep(2)
        print("file copy has now finished")

        roas_calculator = RoasCalculator(event.src_path)
        roas_calculator.clean_data()
        roas_calculator.calculate_roas()
