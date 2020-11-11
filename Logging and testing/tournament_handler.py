# -*- coding: utf-8 -*-
# python 3.8.6

from bowling import ScoreCalculator, FramesQuantityError
from bowling2 import ScoreCalculatorNew


class TournamentCalculator:

    def __init__(self, source, good_log, bad_log, mode='1'):
        """
        :param source: файл протокола турнита
        :param good_log: файл для записи результатов подсчета очков
        """
        self.source = source
        self.good_log = good_log
        self.bad_log = bad_log
        self.mode = mode
        self.scores = {}
        self.winners_table = {}

    def tournament_results(self):
        """
        Функция считает очки из файла протокола турнира и записывает результаты в выходной файл
        """
        self.winners_table = {}
        with open(self.source, 'r', encoding='utf8') as sourcefile:
            with open(self.good_log, 'a', encoding='utf8') as goodlog:
                with open(self.bad_log, 'a', encoding='utf8') as badlog:
                    lines = sourcefile.readlines()
                    for line in lines:
                        line = line.replace('\n', '')
                        if 'Tour' in line:
                            goodlog.write(f"{line}\n")
                            badlog.write(f"{line}\n")
                            continue
                        if 'winner' in line:
                            if self.scores:
                                self.scores = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
                                goodlog.write(f"winner is {self.scores[0][0]}\n")

                                self.winners_table[self.scores[0][0]]['wins'] += 1
                            else:
                                goodlog.write('Can not calculate the score\n')
                            goodlog.write('\n')
                            badlog.write('\n')
                            self.scores.clear()
                            self.scores = {}
                            continue
                        if not line:
                            continue
                        player, score = line.split('\t')
                        try:
                            if self.mode == '1':
                                result = ScoreCalculator().get_score(score)
                            elif self.mode == '2':
                                result = ScoreCalculatorNew().get_score(score)
                            self.scores[player] = result
                            goodlog.write(f"{player} {score} {result}\n")

                            if player in self.winners_table:
                                self.winners_table[player]['matches'] += 1
                            else:
                                self.winners_table[player] = {'matches': 1, 'wins': 0}

                        except (ValueError, FramesQuantityError) as exc:
                            badlog.write(f"{player} {score} {exc}\n")
            self.winners_table = sorted(self.winners_table.items(),
                                        key=lambda res: (res[1]['wins'], res[1]['matches']),
                                        reverse=True)
        print(f'\n\nПроизведена запись в файл {self.good_log}\nПроизведена запись в файл {self.bad_log}\n\n')

    def format_result(self):
        """
        Функция печатает на консоль форматированные результаты турнира
        """
        print(f"+{'-' * 10}+{'-' * 16}+{'-' * 16}+\n"
              f"|{'Игрок':^10}|{'сыграно матчей':^16}|{'всего побед':^16}|\n"
              f"+{'-' * 10}+{'-' * 16}+{'-' * 16}+")
        for player, results in self.winners_table:
            print(f"|{player:^10}|{results['matches']:^16}|{results['wins']:^16}|\n"
                  f"+{'-' * 10}+{'-' * 16}+{'-' * 16}+")

    def run(self):
        self.tournament_results()
        self.format_result()
