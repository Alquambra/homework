import re
import json
from csv import writer
from decimal import Decimal
from datetime import datetime


class Monster:
    """Класс монстр. Объект класса принимает строку с монстром и парсит ее"""
    monster_description = r'(Mob|Boss)_exp(\d+)_tm(\d+)'

    def operate(self, monster):
        monster_re = re.findall(self.monster_description, monster)
        exp = int(monster_re[0][1])
        tm = Decimal(monster_re[0][2])
        return exp, tm


class Location:
    """Класс локация. Объект класса принимает строку с локацией и парсит ее"""
    location_description = r'(Location_\w+|Hatch)_tm([\d+|\d/.]+)'

    def operate(self, location):
        location_re = re.findall(self.location_description, location)
        cur_location = location_re[0][0]
        tm = Decimal(location_re[0][1])
        return cur_location, tm

class Game:
    """Класс Игры. Создает объект - игру"""

    def __init__(self):
        self.monster_class = Monster()
        self.location_class = Location()
        with open('result.csv', 'a', newline='', encoding='utf8') as csv_file:
            csv_writer = writer(csv_file, )
            csv_writer.writerow(['current_location', 'current_experience', 'current_date'])

    def turn(self, game_map, monster_killed, monsters):
        """
        Функция производит один ход игрока
        :param game_map: карта местности, в которой находится игрок
        :param monster_killed: Если игрок убил монстра, то возвращается True и игра продолжается с этого же места
        :return: current_location - текущая локация, monsters - монстры в текущей локации, locations - локации следующие
        за текущей локацией
        """
        locations = []
        for current_location, environment_in in game_map.items():
            if environment_in == "You are winner":
                return 'You are winner'
            for item in environment_in:
                if isinstance(item, dict):
                    locations.append(item)
                elif isinstance(item, str):
                    if monster_killed == False:
                        monsters.append(item)
            return current_location, monsters, locations


    def print_current_state(self, current_location, monsters, locations):
        """
        Функция печатает статус и параметры игры на консоль.
        :param current_location: текущая локация
        :param monsters: монстры в текущей локации
        :param locations: окации следующие за текущей локацией
        :return: available_actions - действия доступные для игрока
        """
        with open('result.csv', 'a', newline='', encoding='utf8') as csv_file:
            csv_writer = writer(csv_file, )
            available_actions = []
            if monsters:
                available_actions.append("Атаковать монстра")
            if locations:
                available_actions.append("Перейти в другую локацию")
            available_actions.append("Сдаться и выйти из игры")

            csv_writer.writerow([current_location, self.current_experience, datetime.now()])

            print(f"\nВы находитесь в {current_location}\nУ вас {self.current_experience} опыта и осталось "
                  f"{self.remaining_time} секунд до наводнения\nПрошло времени: {self.elapsed_time}\n")
            monsters_to_view = list(map(lambda x: '- Монстра: ' + x, monsters))
            locations_to_view = list(map(lambda x: '- Вход в локацию: ' + list(x.keys())[0], locations))
            print("Внутри вы видите:")
            print(*monsters_to_view, sep='\n')
            print(*locations_to_view, sep='\n')
            print(f"Выберите действие:")
            available_actions = list(map(lambda x:
                            str(available_actions.index(x) + 1)
                            + '.'
                            + x,
                            available_actions))
            print(*available_actions, sep='\n')
            return available_actions

    def chooser(self, len_of_available_actions):
        """
        Выбор игроком варианта действия
        :param len_of_available_actions: Длина списка с доступными действиями
        :return: option - возвращает вариант действия
        """
        available_choices = [str(i + 1) for i in range(len_of_available_actions)]
        while True:
            option = input('>>> ')
            if option in available_choices:
                break
        return option

    def attack_monster(self, monsters):
        """
        Функция атаки выбранного монстра из переданного списка. Изменяет артибуты объекта класса
        self.current_experience, self.current_date, self.remaining_time.
        :param monsters - список монстров для атаки
        :return choose - выбор монстра для атаки
        """
        print('\nВы выбрали атаковать монстра\nМонстры для сражения:')
        monsters_for_fight = []
        for i in range(len(monsters)):
            monsters_for_fight.append(str(i + 1) + '.' + monsters[i])
        print(*monsters_for_fight, sep='\n')
        choose = self.chooser(len(monsters))

        exp, tm = self.monster_class.operate(monsters[int(choose) - 1])
        self.current_experience += exp
        self.elapsed_time += tm
        self.remaining_time -= tm

        return choose

    def step_into_location(self, locations):
        """
        Функция выбора локации для перехода. Изменяет атрибут объекта класса self.remaining_time
        :param locations: список локаций доступных для перехода
        :return choose - выбор локации для перехода
        """
        print('\nВы выбрали перейти в другую локацию\nДоступные локации:')
        locations_for_action = \
            list(map(lambda x:
                     str(locations.index(x) + 1)
                     + '.Войти в локацию: '
                     + list(x.keys())[0],
                     locations))
        print(*locations_for_action, sep='\n')
        choose = self.chooser(len(locations))

        curr_location, tm = self.location_class.operate(locations_for_action[int(choose) - 1])
        self.remaining_time -= tm
        self.elapsed_time += tm

        return choose

    def cycle(self):
        """
        Цикл одной полной игры
        :return: 'win' - победа или 'exit' - выход из игры
        """

        self.current_experience = 0
        self.elapsed_time = 0
        self.remaining_time = Decimal('123456.0987654321')
        monsters = []
        monster_killed = False
        with open('rpg.json', 'r', encoding='utf8') as rpg:
            game_map = json.load(rpg)
        while True:
            turn = self.turn(game_map, monster_killed, monsters)
            if turn == 'You are winner':
                if self.current_experience >= 280:
                    print(turn)
                    return "win"
                else:
                    print('\n\n\nВы проиграли\n\n\n\n\nИгра началась заного')
                    return
            else:
                current_location, monsters, locations = turn
                if not locations or self.remaining_time <= 0:
                    print('\n\n\nВы проиграли\n\n\n\n\nИгра началась заного')
                    return
                available_actions_to_print = self.print_current_state(current_location, monsters, locations)

                action = self.chooser(len(available_actions_to_print))
                action = available_actions_to_print[int(action) - 1][2:]
                if action == 'Атаковать монстра':
                    index = int(self.attack_monster(monsters)) - 1
                    monsters.remove(monsters[index])
                    monster_killed = True
                elif action == 'Перейти в другую локацию':
                    index = int(self.step_into_location(locations)) - 1
                    next_location = locations[index]
                    game_map = next_location
                    monster_killed = False
                    monsters = []
                elif action == 'Сдаться и выйти из игры':
                    return 'exit'


    def play(self):
        """
        Игра до победы или сдачи
        """
        try:
            while True:
                win = self.cycle()
                if win in ['win', 'exit']:
                    break
        except KeyboardInterrupt:
            pass
