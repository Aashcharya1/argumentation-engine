"""Executable demonstration; saves actual output with python demo.py > results/demo.txt."""
import json
from engine import ArgumentationFramework, jsonable
from book_examples import example_5_10, example_5_11


def main():
    af = ArgumentationFramework('ab', [('a','b'),('b','a')])
    print('MUTUAL ATTACK: all semantics and legal labellings')
    for semantics in ['grounded','complete','preferred','stable','semi-stable']:
        print(semantics, jsonable(af.extensions(semantics)))
    print('Legal labellings:', af.legal_labellings())
    for label, game in [('Example 5.10', example_5_10()), ('Example 5.11', example_5_11())]:
        print('\n' + label)
        print('Truthful outcome:', jsonable(game.outcome(game.ownership)))
        print('Truthful utilities:', [game.utility(i, game.ownership) for i in range(3)])
        print('Agent x best responses:', jsonable(game.best_responses(0, game.ownership)))
        print('Exact strategyproofness:', json.dumps(jsonable(game.strategyproof())))
        print('Odd-walk condition:', jsonable(game.odd_path_condition()))


if __name__ == '__main__':
    main()
