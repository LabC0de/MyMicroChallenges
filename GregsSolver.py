import random


class GregsSolver:
    def __init__(self, game):
        self.length = len(game.code)
        self.options = game.options
        self.memory = [self.length] + [0 for _ in range(self.options - 1)]
        self.mem_idx = 0

        self.truth_matrix = [[True for _ in range(self.length)] for _ in range(self.options)]

        self.last_guess = []
        self.is_done = False

    def print_truth(self):
        msg = ""
        for num, numrow in enumerate(self.truth_matrix):
            msg += f"{self.memory[num]:3} times{num:3}: "
            for possibility in numrow:
                if possibility:
                    msg += "  x"
                else:
                    msg += "  o"
            msg += "\n"
        return msg

    def done(self):
        return self.is_done

    def shift_guess(self, guess):
        free = [True for _ in range(self.length)]
        shifted = [-1 for _ in range(self.length)]
        for idx, num in enumerate(guess):
            if num == -1:
                continue
            i = idx + 1
            while not free[i] or not self.truth_matrix[num][i]:
                i += 1
            shifted[i] = num
            free[i] = False
        return free, shifted

    def get_guess(self):
        free = [True for _ in range(self.length)]
        guess = [-1 for _ in range(self.length)]
        for num, amount in enumerate(self.memory):
            for _ in range(amount):
                i = 0
                try:
                    while not free[i] or not self.truth_matrix[num][i]:
                        i += 1
                        if i >= len(free):
                            free, guess = self.shift_guess(guess)
                            i = 0
                except IndexError:
                    print(f"{num} {amount} {guess}")
                    print(self.print_truth())
                    raise
                free[i] = False
                guess[i] = num
        print(guess)
        self.last_guess = guess
        return guess

    def eval_result(self, result):
        if result.find("You") != -1:
            self.is_done = True
            print(result)
            print(self.print_truth())
            return
        if result.count("x") == 0:
            for idx, num in enumerate(self.last_guess):
                self.truth_matrix[num][idx] = False
        if result.count("o") == 0:
            for num in self.last_guess:
                for jdx in range(self.length):
                    if self.last_guess[jdx] != num:
                        self.truth_matrix[num][jdx] = False
        if self.mem_idx < self.options:
            self.memory[self.mem_idx] -= (self.length - len(result))
            if self.memory[self.mem_idx] == 0:
                for idx in range(self.length):
                    self.truth_matrix[self.mem_idx][idx] = False
            self.mem_idx += 1
            if self.mem_idx < self.options:
                self.memory[self.mem_idx] += (self.length - len(result))
        print(result)
