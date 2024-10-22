from csv import DictWriter
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from pytz import timezone


class Robots:

    @classmethod
    def save_csv(
            cls,
            values: List[Dict],
            crawler_name: str,
            directory: str = "results"
    ):
        cls.create_directory(directory)
        cls.create_directory(f"{directory}/{crawler_name}")
        filename = datetime.now(
            tz=timezone('America/Sao_Paulo')
        ).strftime(f"{directory}/{crawler_name}/%Y_%m_%d_%H_%M_%S.csv")
        with open(filename, 'w', newline='') as f:
            writer = DictWriter(f, fieldnames=list(values[0].keys()))
            writer.writeheader()
            [writer.writerow(value) for value in values]
        return filename

    @staticmethod
    def create_directory(path: str) -> None:
        """
        This method creates log folder during __init__
        """

        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
