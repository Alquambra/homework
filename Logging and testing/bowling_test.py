import unittest
from bowling import ScoreCalculator
from bowling2 import ScoreCalculatorNew



class ScoreCalculatorTest(unittest.TestCase):

    def test_1(self):
        result = ScoreCalculator().get_score('1/6/1/--327-18812382')
        self.assertEqual(result, 90)

    def test_2(self):
        result = ScoreCalculator().get_score('3532X332/3/62--62X')
        self.assertEqual(result, 105)

    def test_3(self):
        result = ScoreCalculator().get_score('725518X--8/--543152')
        self.assertEqual(result, 83)

    def test_4(self):
        result = ScoreCalculator().get_score('8/--35-47/371/518-4/')
        self.assertEqual(result, 96)

    def test_5(self):
        result = ScoreCalculator().get_score('4-3/7/3/8/X711627-5')
        self.assertEqual(result, 113)

class ScoreCalculatorNewTest(unittest.TestCase):

    def test_1(self):
        result = ScoreCalculatorNew().get_score('1/6/1/--327-18812382')
        self.assertEqual(result, 82)

    def test_2(self):
        result = ScoreCalculatorNew().get_score('3532X332/3/62--62X')
        self.assertEqual(result, 90)

    def test_3(self):
        result = ScoreCalculatorNew().get_score('725518X--8/--543152')
        self.assertEqual(result, 68)

    def test_4(self):
        result = ScoreCalculatorNew().get_score('8/--35-47/371/518-4/')
        self.assertEqual(result, 84)

    def test_5(self):
        result = ScoreCalculatorNew().get_score('4-3/7/3/8/X711627-5')
        self.assertEqual(result, 119)

    def test_6(self):
        result = ScoreCalculatorNew().get_score('811/X--3/XX171/43')
        self.assertEqual(result, 127)

    def test_7(self):
         result = ScoreCalculatorNew().get_score('--8-X3/4/1/-12651X')
         self.assertEqual(result, 88)


if __name__ == '__main__':
    unittest.main()