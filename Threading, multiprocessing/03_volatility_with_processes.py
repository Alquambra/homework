# -*- coding: utf-8 -*-


# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПРОЦЕССНОМ стиле
#
# Бумаги с нулевой волатильностью вывести отдельно.
# Результаты вывести на консоль в виде:
#   Максимальная волатильность:
#       ТИКЕР1 - ХХХ.ХХ %
#       ТИКЕР2 - ХХХ.ХХ %
#       ТИКЕР3 - ХХХ.ХХ %
#   Минимальная волатильность:
#       ТИКЕР4 - ХХХ.ХХ %
#       ТИКЕР5 - ХХХ.ХХ %
#       ТИКЕР6 - ХХХ.ХХ %
#   Нулевая волатильность:
#       ТИКЕР7, ТИКЕР8, ТИКЕР9, ТИКЕР10, ТИКЕР11, ТИКЕР12
# Волатильности указывать в порядке убывания. Тикеры с нулевой волатильностью упорядочить по имени.
#
import zipfile
import os
from multiprocessing import Process, Queue
from queue import Empty
import time

ZIP_FOLDER = 'trades.zip'
FOLDER = ZIP_FOLDER.replace('.zip', '')


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()

        result = func(*args, **kwargs)

        ended_at = time.time()
        elapsed = round(ended_at - started_at, 6)
        print(f'Функция {func.__name__} работала {elapsed} секунд(ы)')
        return result

    return surrogate


for dirname, dirpath, filename in os.walk(FOLDER):
    first = filename[0]


class VolatilityCalculator(Process):

    def __init__(self, file, folder, buffer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file = file
        self.folder = folder
        self.buffer = buffer
        self.price_storage = []

    def run(self):
        with open(os.path.join(self.folder, self.file), 'r', encoding='utf8') as csv:
            csv.readline()
            for line in csv.readlines():
                self.secid, tradetime, self.price, quantity = line.split(',')
                self.price_storage.append(float(self.price))

        half_sum = (max(self.price_storage) + min(self.price_storage)) / 2
        if half_sum:
            self.volatility = (max(self.price_storage) - min(self.price_storage)) / half_sum * 100
            self.volatility = round(self.volatility, 2)
        else:
            self.volatility = 0
        if self.buffer.full():
            print('Буфер заполнен', flush=True)
        self.buffer.put((self.secid, self.volatility))


class ZipVolatilityCalculator(VolatilityCalculator):

    def extracting(self):
        self.zfile = zipfile.ZipFile(self.folder)
        self.zfile.extractall()


class ResultBuffer(Process):

    def __init__(self, folder, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.files = []
        self.folder = folder
        self.ticker_dict = {}
        self.zero_ticker_dict = {}
        self.buffer = Queue()

    def run(self):

        for dirname, dirpath, filename in os.walk(self.folder):
            for file in filename:
                if self.folder in os.listdir(current_path):
                    thread = VolatilityCalculator(file=file, folder=self.folder, buffer=self.buffer)
                else:
                    thread = ZipVolatilityCalculator(file=file, folder=self.folder, buffer=self.buffer)
                self.files.append(thread)

        for thread in self.files:
            thread.start()
        while True:
            try:
                tick, vol = self.buffer.get(timeout=1)
                if vol == 0:
                    self.zero_ticker_dict[tick] = vol
                else:
                    self.ticker_dict[tick] = vol
            except Empty:
                if not any(thread.is_alive() for thread in self.files):
                    break
        self.ticker_dict = [(key, self.ticker_dict[key]) for key in
                       sorted(self.ticker_dict, key=self.ticker_dict.get, reverse=True)]

        self.print_result()  # Я вот о чём =)

    def print_result(self):  # отдельный мето как и было раньше.
        print('\nМаксимальная волатильность:')
        for ticker in self.ticker_dict[:3]:
            print(f'{ticker[0]} - {ticker[1]} %')
        print('\nМинимальная волатильность:')
        for ticker in self.ticker_dict[:-4:-1]:
            print(f'{ticker[0]} - {ticker[1]} %')
        print('\nНулевая волатильность:')
        for key in self.zero_ticker_dict.keys():
            print(key, end=', ')
        print()
        for thread in self.files:
            thread.join()




current_path = os.path.dirname(__file__)


@time_track
def main():
    main_thread = ResultBuffer(FOLDER)
    main_thread.start()
    main_thread.join()


if __name__ == '__main__':
    main()
