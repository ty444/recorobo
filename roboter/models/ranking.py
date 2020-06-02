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

    def save(self):
        """save data to csv file."""
        
        with open(self.csv_file, 'w+') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.column)
            writer.writeheader()

            for name, count in self.data.items():
                writer.writerow({
                    RANKING_COLUMN_NAME: name,
                    RANKING_COLUMN_COUNT: count
                })

    def get_most_popular(self, not_list=None):
        """Fetch the data of the top most ranking.

        Args:
            not_list (list): Excludes the name on the list.

        Returns:
            str: Returns the data of the top most ranking
        """
        if not_list is None:
            not_list = []

        if not self.data:
            return None
        
        sorted_data = sorted(self.data, key=self.data.get, reverse=True)
        for name in sorted_data:
            if name in not_list:
                continue
            return name
        
    def increment(self, name):
        """Increase rank for the give name."""
        self.data[name.title()] += 1
        self.save()


