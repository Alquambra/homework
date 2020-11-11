# -*- coding: utf-8 -*-
# python 3.8.6

# Прибежал менеджер и сказал что нужно срочно изменить правила подсчета очков в игре.
# "Выходим на внешний рынок, а там правила игры другие!" - сказал он.
#
# Правила подсчета очков изменяются так:
#
# Если во фрейме страйк, сумма очков за этот фрейм будет равна количеству сбитых кеглей в этом фрейме (10 кеглей)
# плюс количество фактически сбитых кеглей за два следующих броска шара (в одном или двух фреймах,
# в зависимости от того, был ли страйк в следующем броске).
# Например: первый бросок шара после страйка - тоже страйк, то +10 (сбил 10 кеглей)
# и второй бросок шара - сбил 2 кегли (не страйк, не важно как закончится этот фрейм - считаем кегли) - то еще +2.
#
# Если во фрейме сбит спэр, то сумма очков будет равна количеству сбитых кеглей в этом фрейме (10 кеглей)
# плюс количество фактически сбитых кеглей за первый бросок шара в следующем фрейме.
#
# Если фрейм остался открытым, то сумма очков будет равна количеству сбитых кеглей в этом фрейме.
#
# Страйк и спэр в последнем фрейме - по 10 очков.
#
# То есть для игры «Х4/34» сумма очков равна 10+10 + 10+3 + 3+4 = 40,
# а для игры «ХXX347/21» - 10+20 + 10+13 + 10+7 + 3+4 + 10+2 + 3 = 92

# Необходимые изменения сделать во всех модулях. Тесты - дополнить.

# "И да, старые правила должны остаться! для внутреннего рынка..." - уточнил менеджер напоследок.

import argparse
from tournament_handler import TournamentCalculator


def command_line_handler():
    """
    Функция парсит из командной строки исходный файл и файл записи
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help="Source file")
    parser.add_argument('-o', '--output', help='Destination file')
    parser.add_argument('-b', '--badlog', help='errors log', default='bad_log.txt')
    args = parser.parse_args()
    return args.input, args.output, args.badlog


if __name__ == '__main__':
    mode = input('Choose mode:\n1 for old rules\n2 for new rules\n >>> ')
    while mode not in ['1', '2']:
        print('Invalid input. Try again.')
        mode = input('Choose mode:\n1 for old rules\n2 for new rules\n>>> ')
    inputf, outputf, bad_log = command_line_handler()
    tournament_result = TournamentCalculator(inputf, outputf, bad_log, mode)
    tournament_result.run()

# зачёт!
