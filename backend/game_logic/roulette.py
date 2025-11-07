import random

class Roulette:
    def __init__(self):
        # European roulette with numbers 0-36
        self.numbers = list(range(37))
        self.red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        self.black_numbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

    def spin(self):
        """Spin the roulette wheel"""
        return random.choice(self.numbers)

    def check_bet(self, bet_type, bet_value, result):
        """
        Check if the bet wins and return the payout multiplier
        bet_type can be: 'number', 'red', 'black', 'even', 'odd', 'low', 'high'
        """
        if bet_type == 'number':
            if int(bet_value) == result:
                return 35  # 35:1 payout
            return 0

        elif bet_type == 'red':
            if result in self.red_numbers:
                return 1  # 1:1 payout
            return 0

        elif bet_type == 'black':
            if result in self.black_numbers:
                return 1  # 1:1 payout
            return 0

        elif bet_type == 'even':
            if result != 0 and result % 2 == 0:
                return 1  # 1:1 payout
            return 0

        elif bet_type == 'odd':
            if result != 0 and result % 2 == 1:
                return 1  # 1:1 payout
            return 0

        elif bet_type == 'low':  # 1-18
            if 1 <= result <= 18:
                return 1  # 1:1 payout
            return 0

        elif bet_type == 'high':  # 19-36
            if 19 <= result <= 36:
                return 1  # 1:1 payout
            return 0

        return 0

    def get_color(self, number):
        """Get the color of a number"""
        if number == 0:
            return 'green'
        elif number in self.red_numbers:
            return 'red'
        else:
            return 'black'
