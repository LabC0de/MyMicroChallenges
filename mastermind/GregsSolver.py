

class GregsSolver:
    def __init__(self, game, benchmark=False):
        self.debug = f"{game.code}\n"

        self.bm = benchmark
        self.length = len(game.code)
        self.options = game.options

        self.memory = [self.length] + [0 for _ in range(self.options - 1)]
        self.mem_idx = 0

        self.found_colors = 0
        self.edge_case_possible = True

        self.iter_map = [list(range(self.options)) for _ in range(self.length)]

        self.last_guess = [0 for _ in range(self.length)]
        self.is_done = False

        self.logic_history = []
        self.right_history = []

    def print_truth(self):
        msg = ""
        for num, numrow in enumerate(self.iter_map):
            msg += f"position {num}: "
            for possibility in numrow:
                msg += f"{possibility:3} "
            msg += "\n"
        msg += "number:     "
        for num in range(self.options):
            msg += f"{num:3}"
        msg += "\noccurances: "
        for num in self.memory:
            msg += f"{num:3}"
        return msg + "\n"

    def print_history(self):
        msg = ""
        for i, guess in enumerate(self.logic_history):
            for num in guess:
                msg += f"{num:3} "
            msg += f"<< x:{self.right_history[i]:3}\n"
        return msg

    def __discard(self, idx, num):
        try:
            self.iter_map[idx].remove(num)
        except ValueError:
            return

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
                self.__discard(idx, num)
        if right_color == 0:
            for idx, num in enumerate(self.last_guess):
                if len(self.iter_map[idx]) != 1:
                    if num < self.mem_idx:
                        self.iter_map[idx] = [num]
                    for jdx in range(self.length):
                        if self.last_guess[jdx] != num:
                            self.__discard(jdx, num)
        if self.mem_idx < self.options:
            if self.memory[self.mem_idx] == 0:
                for idx in range(self.length):
                    self.__discard(idx, self.mem_idx)
            else:
                self.found_colors += 1
            if self.edge_case_possible:
                if self.found_colors == 1:
                    if self.memory[self.mem_idx] != 1:
                        self.edge_case_possible = False
                elif self.found_colors == 2:
                    if (spot_on == 0) or (right_color == 0) or (spot_on > 1):
                        self.edge_case_possible = False
                        return
                    elif right_color == 1:
                        for idx, num in enumerate(self.last_guess):
                            if num < self.mem_idx:
                                self.__discard(idx, num)
                                self.__discard(idx, self.mem_idx)
                                break
                    else:
                        for idx, num in enumerate(self.last_guess):
                            if num < self.mem_idx:
                                self.iter_map[idx] = [self.mem_idx]
                                break
                    self.edge_case_possible = False

    def __do_history_logic(self):
        if len(self.logic_history) >= 2:
            i = 0
            for idx in range(self.length):
                if (self.logic_history[-1][idx] == self.logic_history[-2][idx]) and (len(self.iter_map[idx]) == 1):
                    i = idx
                    continue
                break
            if self.logic_history[-1][i] > self.logic_history[-2][i]:
                for reject in range(self.logic_history[-1][i]):
                    self.__discard(i, reject)

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

    def __guess_tree(self, guess, mem_cpy, cs, depth=0):
        continued_state = cs
        if depth == self.length:
            return self.__check_against_history(guess)
        for num in self.iter_map[depth]:
            if num < continued_state:
                continue
            elif num == continued_state:
                cs = self.last_guess[(depth + 1) % self.length]
            else:
                cs = -1
            if mem_cpy[num]:
                mem_cpy[num] -= 1
                guess[depth] = num
                if self.__guess_tree(guess, mem_cpy, cs, depth + 1):
                    return True
                mem_cpy[num] += 1
        return False

    def __guess_tree_init(self):
        mem_cpy = [x for x in self.memory]
        guess = [-1 for _ in range(self.length)]
        if self.is_done:
            return self.last_guess
        valid = self.__guess_tree(guess, mem_cpy, self.last_guess[0])
        if not valid:
            print(f"Code: {self.debug}Last Guess: {self.last_guess}\nCurrent Guess: {guess}")
            print(self.print_truth() + self.print_history())
            raise IndexError
        return guess

    def done(self):
        return self.is_done

    def get_guess(self):
        guess = self.__guess_tree_init()
        if self.last_guess[0] > guess[0]:
            print(guess)
        self.last_guess = guess
        return guess

    def eval_result(self, result):
        if not self.bm:
            print(f"{self.last_guess} {result}")
        # else:
            # self.debug += f"{self.print_truth()}{self.last_guess} {result}\n"
        if result.find("You") != -1:
            self.is_done = True
            if not self.bm:
                print(self.print_truth() + self.print_history())
                print(f"{result}")
            return
        if self.mem_idx < self.options:
            self.memory[self.mem_idx] -= (self.length - len(result))
            self.__note_in_table(result.count("x"), result.count("o"))
            self.__add_to_history(result.count("x"))
            self.__do_history_logic()
            self.mem_idx += 1
            if self.mem_idx < self.options:
                self.memory[self.mem_idx] += (self.length - len(result))
        else:
            self.__note_in_table(result.count("x"), result.count("o"))
            self.__add_to_history(result.count("x"))
            self.__do_history_logic()
