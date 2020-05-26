"""Generates ranking model to write to CSV

TODO (ty444) Rewrite to DB instead of CSV
"""

import collections
import csv
import os
import pathlib


RANKING_COLUMN_NAME = 'LANG NAME'
RANKING_COLUMN_COUNT = 'COUNT'
RANKING_CSV_FILE_PATH = 'ranking.csv'

class CsvModel(object):
    """Base csv model."""
    def __init__(self, csv_file):
        self.csv_file = csv_file
        if not os.path.exists(csv_file):
            pathlib.Path(csv_file).touch()

class RankingModel(CsvModel):
    """Definition of class that generates ranking model to write to CSV"""
    def __init__(self, csv_file=None, *args, **kargs):
        if not csv_file:
            csv_file = self.get_csv_file_path()
        super().__init__(csv_file, *args, **kargs)
        self.column = [RANKING_COLUMN_NAME, RANKING_COLUMN_COUNT]
        self.data = collections.defaultdict(int)
        self.load_data()

    def get_csv_file_path(self):
        """set csv file path.

        Use csv path if set in settings, otherwise use default
        """
        csv_file_path = None
        try:
            import settings
            if settings.CSV_FILE_PATH:
                csv_file_path = settings.CSV_FILE_PATH
        except ImportError:
            pass

        if not csv_file_path:
            csv_file_path = RANKING_CSV_FILE_PATH
        return csv_file_path

    def load_data(self):
        """Load csv data.

        Returns:
            dict: Return ranking data of dict type.
        """
        with open(self.csv_file, 'r+') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                self.data[row[RANKING_COLUMN_NAME]] = int(
                    row[RANKING_COLUMN_COUNT])
        return self.data

    
