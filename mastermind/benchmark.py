import Mastermind
import argparse
import importlib
from timeit import default_timer as timer


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--solver", type=str, required=True,
                        help="sets the solver for the game. Defaults to manual player.")
    parser.add_argument("-m", "--module", type=str, default=None,
                        help="specifies the module for your autosolver. If not specified its assumed that your autosolver is called like it's module.")
    args = parser.parse_args()
    if args.module is None:
        globals().update(importlib.import_module(args.solver).__dict__)
    else:
        globals().update(importlib.import_module(args.module).__dict__)
    levels = [(10, 4, 6), (10, 5, 8), (12, 6, 8), (12, 8, 10)]
    for level in levels:
        try:
            performance = {"lost": 0, "sum": 0, "avg time": 0.0}
            mastermind = Mastermind.Game(*level)
            samples = level[2] ** level[1]
            if samples > 10000:
                samples = 10000
            for sample in range(samples):
                player = globals()[args.solver](mastermind, True)
                start = timer()
                while True:
                    guess = player.get_guess()
                    if player.done():
                        break
                    player.eval_result(mastermind.do_turn(mastermind.do_input(guess)))
                end = timer()
                won, tries, colors, codelen = mastermind.get_last_score()
                performance["sum"] += 1
                performance["avg time"] = performance["avg time"] * (performance["sum"] - 1)/performance["sum"] + (end - start)/performance["sum"]
                if not won:
                    performance["lost"] += 1
                if performance.get(tries):
                    performance[tries] += 1
                else:
                    performance[tries] = 1
        except KeyboardInterrupt:
            print(f"Performance on code of length {codelen} with {colors} possibilities: {performance}")
            exit(-1)
        print(f"Performance on code of length {codelen} with {colors} possibilities: {performance}")
