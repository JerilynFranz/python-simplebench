#!python3
'''A minimal example of using simplebench.'''
import sys

from simplebench import benchmark, main


@benchmark
def addition_benchmark():
    '''A simple addition benchmark.'''
    sum(range(1000))


@benchmark('string_ops', title='String Concatenation Benchmark')
def string_concatenation_benchmark():
    '''A simple string concatenation benchmark.'''
    result = ''
    for i in range(1000):
        result += str(i)


if __name__ == '__main__':
    extra_args = None if len(sys.argv) > 1 else ['--progress', '--rich-table.console']
    main(extra_args=extra_args)
