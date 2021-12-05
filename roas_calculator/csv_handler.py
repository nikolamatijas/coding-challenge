import logging

from watchdog.events import PatternMatchingEventHandler, FileCreatedEvent

from roas_calculator.roas_calculator import RoasCalculator


class CsvHandler(PatternMatchingEventHandler):
    """
    CsvHandler is class inherited from watchdog.events.PatternMatchingEventHandler class.
    This class can be configured to react on any kind of file system movement and for every kind of file pattern.
    Instances of CsvHandler class will only react on created CSV files.
    """

    def __init__(self):
        """
        The constructor for CsvHandler class. Handler is configured to react only on .csv files.
        """
        PatternMatchingEventHandler.__init__(self, patterns=['*.csv'],
                                             ignore_directories=True, case_sensitive=False)

    def on_created(self, event: FileCreatedEvent):
        """
        This function will be triggered every time when new CSV file is created.
        It will try to calculate ROAS for search terms from CSV file.
        """
        logging.info('Detected new CSV file %s', event.src_path)
        roas_calculator = RoasCalculator(event.src_path)
        if (roas_calculator.data_frame is not None) and (roas_calculator.validate_data_frame_columns()):
            roas_calculator.clean_data_frame()
            roas_calculator.calculate_roas()
            logging.info('ROAS for search terms from %s file is calculated.', event.src_path)
