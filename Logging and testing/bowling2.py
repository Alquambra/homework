from bowling import FramesQuantityError


class ScoreCalculatorNew:

    def __init__(self):
        """
        :param game_result: строка с записью результатов игры вида Антон\t1/6/1/--327-18812382
        """
        # self.game_result = game_result
        self.symbols = []
        self.allowed_symbols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'X', 'Х', '/', '-']
        self.frames = 0
        self.score = 0

    def get_score(self, game_result, strike=False, spare=False):
        """
        Функция конвертирует строку game_result в количество очков игрока
        :return: self.score
        """

        for place, symbol in enumerate(game_result):
            if symbol not in self.allowed_symbols:
                raise ValueError \
                    ("Symbol not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'X', 'Х', '/', '-']")
            self.symbols.append(symbol)
            if len(self.symbols) == 2:
                if self.symbols[0] == '/':
                    raise ValueError(f"Invalid input {''.join(self.symbols)} must be 'X'")
                elif self.symbols[1] == '/':
                    if strike:
                        return 10
                    self.frames += 1

                    spare = True
                    if spare:
                        self.symbols.clear()
                        slice = game_result[place + 1: place + 3]
                        if slice:
                            self.score += self.get_score(game_result[place + 1] + '-', spare=True) + 10
                        else:
                            self.score += 10
                        spare = False
                else:
                    frame_score = sum(int(i) for i in self.symbols if i != '-')
                    if strike or spare:
                        return frame_score
                    self.score += frame_score
                    if frame_score == 10:
                        raise ValueError(f"Invalid input: {''.join(self.symbols)} must be {self.symbols[0]}/")
                    self.frames += 1
                self.symbols.clear()
            elif symbol == 'X':
                if spare:
                    return 10
                if strike:
                    strike = False
                    if game_result == 'X':
                        return 10
                    else:
                        return 10 + int(game_result[1])

                strike = True
                if strike:
                    self.symbols.clear()
                    slice = game_result[place + 1:place + 3]
                    if slice:
                        self.score += self.get_score(slice, strike=True) + 10
                    else:
                        self.score += 10
                    strike = False

                self.frames += 1
                self.symbols.clear()
        if self.frames != 10 and not (strike or spare):
            raise FramesQuantityError(frames=self.frames)
        else:
            return self.score
