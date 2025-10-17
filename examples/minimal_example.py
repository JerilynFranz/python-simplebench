#!python3
'''A minimal example of using simplebench.'''
import sys

from simplebench import benchmark, main


@benchmark()
def addition_benchmark():
    '''A simple addition benchmark.'''
    sum(range(1000))


if __name__ == '__main__':
    extra_args = None if len(sys.argv) > 1 else ['--progress', '--rich-table.console']
    main(extra_args=extra_args)
