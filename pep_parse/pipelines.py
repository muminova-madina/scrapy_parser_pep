import csv
import logging
from datetime import datetime as dt

from pep_parse.constants import DT_FORMAT, BASE_DIR


class PepParsePipeline:

    def open_spider(self, spider):
        self.status = {}

    def process_item(self, item, spider):
        if 'status' not in item:
            logging.error("Не полные данные: нет ключа 'status'")
            return item

        key = item['status']
        self.status[key] = self.status.get(key, 0) + 1
        return item

    def close_spider(self, spider):
        results_dir = BASE_DIR / 'results'
        results_dir.mkdir(exist_ok=True)
        now_time = dt.now().strftime(DT_FORMAT)
        file_name = results_dir / f'status_summary_{now_time}.csv'
        with open(file_name, mode='w', encoding='utf-8') as file:
            writer = csv.writer(
                file, dialect='unix', delimiter=';'
            )
            writer.writerows(
                (
                    ('Статус', 'Количество'),
                    *self.status.items(),
                    ('Total', sum(self.status.values()))
                )
            )
