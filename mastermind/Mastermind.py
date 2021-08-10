#-*-coding:utf8;-*-
#qpy:3
#qpy:console
import re
import random
import argparse
import importlib


class ManualPlayer:
    def __init__(self, game):
        print("Playing a game of mastermind.\nCode length is {}.\nOptions are the numbers 0-{}.\nYou have {} guesses.\nGood Luck!".format(len(game.code), game.options - 1, game.rows)) 
        self.is_done = False
    
    def done(self):
        return self.is_done
    
    def get_guess(self):
        ip = input()
        if ip == "q":
            self.is_done = True
        return re.sub(r"[,:.; ]+", " ", ip).strip().split()
    
    def eval_result(self, result):
        print(result) 


class InputError(Exception):
    def __init__(self, message):
        print(message) 


class Game:
    def __init__(self, rows, columns, options):
        self.rows = rows
        self.trys = 0
        self.last_tries = 0
        self.code = list()
        self.options = options
        self.won = False
        self.mp = [0 for _ in range(options)]
        for i in range(columns):
            self.code.append(random.randint(0, options - 1))
            self.mp[self.code[-1]] += 1

    def set_code(self, code):
            if len(code) != len(self.code):
                return
            self.code = [int(x) for x in code]
            for i, _ in enumerate(self.mp):
                self.mp[i] = 0
            for i, _ in enumerate(self.code):
                self.mp[self.code[i]] += 1

    def restart(self):
        self.last_tries = self.trys
        self.trys = 0
        for i, _ in enumerate(self.mp):
            self.mp[i] = 0
        for i, _ in enumerate(self.code):
            self.code[i] = random.randint(0, self.options - 1)
            self.mp[self.code[i]] += 1

    def get_last_score(self):
        return self.won, self.last_tries, self.options, len(self.code)

    def do_input(self, ip):
        if len(ip) != len(self.code):
            raise InputError("Input of wrong length") 
        for i, n in enumerate(ip):
            try:
                ip[i] = int(n)
                if ip[i] >= self.options:
                    raise InputError("Inputs must be smaller than {}".format(self.options)) 
            except ValueError:
                raise InputError("Inputs need to be a {} numbers between 0-{}.".format(len(self.code), self.options-1))
        return ip
        
    def do_turn(self, guess):
        result = ""
        self.trys += 1
        tmp = [0 for x in range(self.options)]
        for i, x in enumerate(guess):
            tmp[x] += 1
            if self.code[i] == x:
                result += "x"
        ctr = 0
        for i, x in enumerate(tmp):
            if x >= self.mp[i]:
                ctr += self.mp[i]
            else:
                ctr += x
        for i in range(ctr - len(result)):
            result += "o"
        if result == "x" * len(self.code):
            self.won = True
            msg = "You won after {} turns".format(self.trys)
            self.restart()
            return msg
        if self.rows != 0:
            if self.rows <= self.trys:
                self.won = False
                msg = "You lost after {} turns. The code was {}".format(self.rows, self.code)
                self.restart()
                return msg
        return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tries", type=int, default=10, help="sets the amount of tries you have. Default 10")
    parser.add_argument("-l", "--lenght", type=int, default=5, help="sets the length of the code to guess. Default 5")
    parser.add_argument("-o", "--options", type=int, default=8, help="sets the amount of numbers that can appear in the code. Default 8") 
    parser.add_argument("-s", "--solver", type=str, default="ManualPlayer", help="sets the solver for the game. Defaults to manual player.") 
    parser.add_argument("-m", "--module", type=str, default=None, help="specifies the module for your autosolver. If not specified its assumed that your autosolver is called like it's module.")
    parser.add_argument("-c", "--code", nargs="+", type=int, default=None, help="Sets the code for the game")
    args = parser.parse_args()
    if args.solver != "ManualPlayer":
        if args.module is None:
            globals().update(importlib.import_module(args.solver).__dict__)
        else:
            globals().update(importlib.import_module(args.module).__dict__) 
    mastermind = Game(args.tries, args.lenght, args.options)
    if args.code is not None:
        mastermind.set_code(args.code)
    player = globals()[args.solver](mastermind) 
    print(mastermind.code)
    while True:
        guess = player.get_guess()
        if player.done():
            break
        try:
            player.eval_result(mastermind.do_turn(mastermind.do_input(guess)))
        except InputError as e:
            continue
