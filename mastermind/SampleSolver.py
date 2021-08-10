import random


class SampleSolver:
    def __init__(self, game, benchmark=False):
        self.length = len(game.code)
        self.options = game.options
        self.is_done = False

    def done(self):
        return self.is_done

    def get_guess(self):
        guess = [random.randint(0, self.options - 1) for _ in range(self.length)]
        print(guess)
        return guess
    
    def eval_result(self, result):
        if result.find("You") != -1:
            self.is_done = True
        print(result)
