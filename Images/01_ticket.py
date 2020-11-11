# -*- coding: utf-8 -*-


# Заполнить все поля в билете на самолет.
# Создать функцию, принимающую параметры: ФИО, откуда, куда, дата вылета,
# и заполняющую ими шаблон билета Airline.
# Шаблон взять в файле lesson_013/images/ticket_template.png
# Пример заполнения lesson_013/images/ticket_sample.png
# Подходящий шрифт искать на сайте ofont.ru

from PIL import Image, ImageFont, ImageDraw
import argparse
import os

dir_for_save = os.path.join(os.getcwd(), )


def make_ticket(fio, from_, to, date, save_dir):
    with Image.open('images/ticket_template.png') as im:
        draw = ImageDraw.Draw(im)

        font = ImageFont.truetype('ofont.ru_Ubuntu.ttf', 14)

        draw.text((45, 128), fio, font=font, fill='black')
        draw.text((45, 197), from_, font=font, fill='black')
        draw.text((45, 263), to, font=font, fill='black')
        draw.text((285, 263), date, font=font, fill='black')

        im.save(save_dir)


parser = argparse.ArgumentParser()

parser.add_argument('fio', help='Input name of the passenger')
parser.add_argument('dep', help='Input departure city')
parser.add_argument('dest', help='Input destination city')
parser.add_argument('date', help='Input date of flight')
parser.add_argument('-s', '--save_to', help='Input path to save', default='ticket.png')

args = parser.parse_args()

make_ticket(fio=args.fio.upper(), from_=args.dep.upper(), to=args.dest.upper(), date=args.date, save_dir=args.save_to)

# make_ticket(fio='ИВАНОВ И.И.', from_='ЗЕМЛЯ', to='ЛУНА', date='09.12')

# Дмитрий, напишите пожалуйста команду для запуска из консоли, которой Вы проверяете корректность работы =)
# python 01_ticket.py "Иванов И.И." земля луна 09.12 -s ticket_to_moon.png

# Усложненное задание (делать по желанию).
# Написать консольный скрипт c помощью встроенного python-модуля argparse.
# Скрипт должен принимать параметры:
#   --fio - обязательный, фамилия.
#   --from - обязательный, откуда летим.
#   --to - обязательный, куда летим.
#   --date - обязательный, когда летим.
#   --save_to - необязательный, путь для сохранения заполненнего билета.
# и заполнять билет.

# зачёт!
