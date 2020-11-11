# -*- coding: utf-8 -*-


# Описание предметной области:
#
# При торгах на бирже совершаются сделки - один купил, второй продал.
# Покупают и продают ценные бумаги (акции, облигации, фьючерсы, етс). Ценные бумаги - это по сути долговые расписки.
# Ценные бумаги выпускаются партиями, от десятка до несколько миллионов штук.
# Каждая такая партия (выпуск) имеет свой торговый код на бирже - тикер - https://goo.gl/MJQ5Lq
# Все бумаги из этой партии (выпуска) одинаковы в цене, поэтому говорят о цене одной бумаги.
# У разных выпусков бумаг - разные цены, которые могут отличаться в сотни и тысячи раз.
# Каждая биржевая сделка характеризуется:
#   тикер ценнной бумаги
#   время сделки
#   цена сделки
#   обьем сделки (сколько ценных бумаг было куплено)
#
# В ходе торгов цены сделок могут со временем расти и понижаться. Величина изменения цен называтея волатильностью.
# Например, если бумага №1 торговалась с ценами 11, 11, 12, 11, 12, 11, 11, 11 - то она мало волатильна.
# А если у бумаги №2 цены сделок были: 20, 15, 23, 56, 100, 50, 3, 10 - то такая бумага имеет большую волатильность.
# Волатильность можно считать разными способами, мы будем считать сильно упрощенным способом -
# отклонение в процентах от полусуммы крайних значений цены за торговую сессию:
#   полусумма = (максимальная цена + минимальная цена) / 2
#   волатильность = ((максимальная цена - минимальная цена) / полусумма) * 100%
# Например для бумаги №1:
#   half_sum = (12 + 11) / 2 = 11.5
#   volatility = ((12 - 11) / half_sum) * 100 = 8.7%
# Для бумаги №2:
#   half_sum = (100 + 3) / 2 = 51.5
#   volatility = ((100 - 3) / half_sum) * 100 = 188.34%
#
# В реальности волатильность рассчитывается так: https://goo.gl/VJNmmY
#
# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью.
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
# Подготовка исходных данных
# 1. Скачать файл https://drive.google.com/file/d/1l5sia-9c-t91iIPiGyBc1s9mQ8RgTNqb/view?usp=sharing
#       (обратите внимание на значок скачивания в правом верхнем углу,
#       см https://drive.google.com/file/d/1M6mW1jI2RdZhdSCEmlbFi5eoAXOR3u6G/view?usp=sharing)
# 2. Раззиповать средствами операционной системы содержимое архива
#       в папку python_base/lesson_012/trades
# 3. В каждом файле в папке trades содержится данные по сделакам по одному тикеру, разделенные запятыми.
#   Первая строка - название колонок:
#       SECID - тикер
#       TRADETIME - время сделки
#       PRICE - цена сделки
#       QUANTITY - количество бумаг в этой сделке
#   Все последующие строки в файле - данные о сделках
#
# Подсказка: нужно последовательно открывать каждый файл, вычитывать данные, высчитывать волатильность и запоминать.
# Вывод на консоль можно сделать только после обработки всех файлов.
#
# Для плавного перехода к мультипоточности, код оформить в обьектном стиле, используя следующий каркас
#
# class <Название класса>:
#
#     def __init__(self, <параметры>):
#         <сохранение параметров>
#
#     def run(self):
#         <обработка данных>

import zipfile
import os
import time

ZIP_FOLDER = 'trades.zip'
FOLDER = ZIP_FOLDER.replace('.zip', '')


def time_track(func):
    """
    Подсчет времени работы декорируемой функции
    """
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


class VolatilityCalculator:

    def __init__(self, file, folder):
        self.file = file
        self.folder = folder
        self.price_storage = []

    def create_prices_list(self):
        """
        Метод читает строку из csv файла и добавляет цену в список с ценами
        """
        with open(os.path.join(self.folder, self.file), 'r', encoding='utf8') as csv:
            csv.readline()
            for line in csv.readlines():
                self.secid, tradetime, self.price, quantity = line.split(',')
                # print(secid, tradetime, price, quantity, sep=' | ')
                self.price_storage.append(float(self.price))

    def calculate(self):
        """
        Метод рассчитывает волатильность из списка с ценами для одного файла
        """
        half_sum = (max(self.price_storage) + min(self.price_storage)) / 2
        if half_sum:
            self.volatility = (max(self.price_storage) - min(self.price_storage)) / half_sum * 100
            self.volatility = round(self.volatility, 2)
        else:
            self.volatility = 0
        return self.secid, self.volatility

    def run(self):
        self.create_prices_list()
        return self.calculate()


class ZipVolatilityCalculator(VolatilityCalculator):

    def extracting(self):
        self.zfile = zipfile.ZipFile(self.folder)
        self.zfile.extractall()


class VolatilityResult:

    def __init__(self, volatility_calculator_list):
        self.volatility_calculator_list = volatility_calculator_list
        self.ticker_dict = {}
        self.zero_ticker_dict = {}

    def sort_result(self):
        """
        Метод складывает волатильности с нулевым значением в один словарь, с ненулевым - в другой
        """
        for ticker in self.volatility_calculator_list:
            tick, vol = ticker.run()
            if vol == 0:
                self.zero_ticker_dict[tick] = vol
            else:
                self.ticker_dict[tick] = vol

    def print_result(self):
        """
        Печать результата в консоль
        """
        ticker_dict = [(key, self.ticker_dict[key]) for key in
                       sorted(self.ticker_dict, key=self.ticker_dict.get, reverse=True)]
        print('\nМаксимальная волатильность:')
        for ticker in ticker_dict[:3]:
            print(f'{ticker[0]} - {ticker[1]} %')
        print('\nМинимальная волатильность:')
        for ticker in ticker_dict[:-4:-1]:
            print(f'{ticker[0]} - {ticker[1]} %')
        print('\nНулевая волатильность:')
        for key in self.zero_ticker_dict.keys():
            print(key, end=', ')
        print()

    def run(self):
        self.sort_result()
        self.print_result()


volatility_calculator_list = []

current_path = os.path.dirname(__file__)


@time_track
def main():
    for dirname, dirpath, filename in os.walk(FOLDER):
        for file in filename:
            if FOLDER in os.listdir(current_path):
                volatility_calculator_list.append(VolatilityCalculator(file, FOLDER))
            else:
                volatility_calculator_list.append(ZipVolatilityCalculator(file, FOLDER))

    result = VolatilityResult(volatility_calculator_list)
    result.run()


main()

# зачёт!
