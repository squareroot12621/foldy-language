"""Foldy: A 1D programming language that doesn't stay 1D.
For more information, see the README.md at
https://github.com/squareroot12621/foldy-language/blob/main/README.md .
"""

from foldy.interpreter import *
import argparse

if __name__ == '__main__': # Run directly
    parser = argparse.ArgumentParser(
        description="Runs Foldy, a 1D programming language "
                    "that doesn't stay 1D.",
        formatter_class=lambda prog: argparse.HelpFormatter(
                            prog, max_help_position=30
                        )
    )
    parser.add_argument('code',
                        help='The Foldy code to be run.',
                        type=str)
    parser.add_argument('-c', '--check',
                        help='show grid and flags before running code',
                        action='store_true')
    parser.add_argument('-i', '--iterations',
                        help='runs for ITER iterations; 0 = runs forever '
                             '(DEFAULT: 50000)',
                        metavar='ITER',
                        type=int,
                        default=50000)
    arguments = parser.parse_args(sys.argv[1:] or ['-h'])
    
    grid = FoldyGrid(arguments.code)
    if arguments.check:
        print(f'\nGrid:\n{grid}\n')
        print(f'Arguments:\n'
              f'-i, --iterations: {arguments.iterations}'
              f'\n')
        grid_checked = input('Type "no" (without quotes) to cancel execution.\n'
                             'Type anything else to continue.\n')
        if grid_checked.strip().casefold() != 'no':
            grid.run(arguments.iterations)
    else:
        grid.run(arguments.iterations)
