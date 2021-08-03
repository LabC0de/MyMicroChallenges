

class GregsSolver:
    def __init__(self, game):
        self.length = len(game.code)
        self.options = game.options
        self.memory = [self.length] + [0 for _ in range(self.options - 1)]
        self.mem_idx = 0

        self.truth_matrix = [[True for _ in range(self.length)] for _ in range(self.options)]

        self.last_guess = []
        self.is_done = False

        self.logic_history = []
        self.right_history = []

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

    def print_history(self):
        msg = ""
        for i, guess in enumerate(self.logic_history):
            for num in guess:
                msg += f"{num:3} "
            msg += f"<< x:{self.right_history[i]:3}\n"
        return msg

    def __add_to_history(self, spot_on):
        if spot_on == 0:
            return
        if self.last_guess.count(self.mem_idx) == len(self.last_guess):
            return
        if self.mem_idx >= self.length:
            candidate = [x for x in self.last_guess]
        elif self.memory[self.mem_idx]:
            candidate = [x for x in self.last_guess]
        else:
            candidate = [x if x != self.mem_idx else -1 for x in self.last_guess]
        if self.logic_history:
            if candidate == self.logic_history[-1]:
                return
        self.logic_history.append(candidate)
        self.right_history.append(spot_on)

    def __note_in_table(self, spot_on, right_color):
        if spot_on == 0:
            for idx, num in enumerate(self.last_guess):
                self.truth_matrix[num][idx] = False
        if right_color == 0:
            for num in self.last_guess:
                for jdx in range(self.length):
                    if self.last_guess[jdx] != num:
                        self.truth_matrix[num][jdx] = False
        if self.mem_idx < self.options:
            if self.memory[self.mem_idx] == 0:
                for idx in range(self.length):
                    self.truth_matrix[self.mem_idx][idx] = False

    def __check_against_history(self, guess):
        for idx, prev_guess in enumerate(self.logic_history):
            ctr = 0
            if prev_guess == guess:
                return False
            for jdx, num in enumerate(prev_guess):
                if num == guess[jdx]:
                    ctr += 1
            if ctr != self.right_history[idx]:
                return False
        return True

    def __guess_tree(self, guess, mem_cpy, depth=0):
        if depth == self.length:
            if self.last_guess == guess:
                return False
            return self.__check_against_history(guess)
        for num in range(self.options):
            if mem_cpy[num] and self.truth_matrix[num][depth]:
                mem_cpy[num] -= 1
                guess[depth] = num
                if self.__guess_tree(guess, mem_cpy, depth + 1):
                    return True
                mem_cpy[num] += 1
        return False

    def __guess_tree_init(self):
        if self.is_done:
            return self.last_guess
        mem_cpy = [x for x in self.memory]
        guess = [-1 for _ in range(self.length)]
        valid = self.__guess_tree(guess, mem_cpy)
        if not valid:
            print(guess)
            print(self.print_truth())
            raise IndexError
        return guess

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
                i = (i + 1) % self.length
            shifted[i] = num
            free[i] = False
        return free, shifted

    def get_guess(self):
        guess = self.__guess_tree_init()
        self.last_guess = guess
        return guess

    def eval_result(self, result):
        print(f"{self.last_guess} {result}")
        if result.find("You") != -1:
            self.is_done = True
            print(self.print_truth() + self.print_history())
            print(f"{result}")
            return
        if self.mem_idx < self.options:
            self.memory[self.mem_idx] -= (self.length - len(result))
            self.__note_in_table(result.count("x"), result.count("o"))
            self.__add_to_history(result.count("x"))
            self.mem_idx += 1
            if self.mem_idx < self.options:
                self.memory[self.mem_idx] += (self.length - len(result))
        else:
            self.__note_in_table(result.count("x"), result.count("o"))
            self.__add_to_history(result.count("x"))
