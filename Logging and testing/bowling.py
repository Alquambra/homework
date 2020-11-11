# -*- coding: utf-8 -*-
# python 3.8.6


class FramesQuantityError(Exception):
    """
    Класс ошибки. Вызывается если строка с результатом game_result(21 строка) содержит недопустимый символ
    """

    def __init__(self, frames):
        self.frames = frames

    def __str__(self):
        return f"Frames quantity must be 10. Now {self.frames}"


class ScoreCalculator:

    def __init__(self):
        """
        :param game_result: строка с записью результатов игры вида Антон\t1/6/1/--327-18812382
        """
        # self.game_result = game_result
        self.symbols = []
        self.allowed_symbols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'X', 'Х', '/', '-']
        self.frames = 0
        self.score = 0

    def get_score(self, game_result):
        """
        Функция конвертирует строку game_result в количество очков игрока
        :return: self.score
        """
        for symbol in game_result:
            if symbol not in self.allowed_symbols:
                raise ValueError \
                    ("Symbol not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'X', 'Х', '/', '-']")
            self.symbols.append(symbol)
            if len(self.symbols) == 2:
                if self.symbols[0] == '/':
                    raise ValueError(f"Invalid input {''.join(self.symbols)} must be 'X'")
                elif self.symbols[1] == '/':
                    self.score += 15
                    self.frames += 1
                else:
                    frame_score = sum(int(i) for i in self.symbols if i != '-')
                    self.score += frame_score
                    if frame_score == 10:
                        raise ValueError(f"Invalid input: {''.join(self.symbols)} must be {self.symbols[0]}/")
                    self.frames += 1
                self.symbols.clear()
            if symbol == 'X':
                self.score += 20
                self.frames += 1
                self.symbols.clear()
        if self.frames != 10:
            raise FramesQuantityError(frames=self.frames)
        return self.score

#  На всякий случай несколько примеров для тестов
#  Антон	1/6/1/--327-18812382
#  Елена	3532X332/3/62--62X => 105 верно
#  Роман	725518X--8/--543152
#  Татьяна	8/--35-47/371/518-4/
#  Ринат	4-3/7/3/8/X711627-5 => 113 верно
