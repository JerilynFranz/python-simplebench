#!python3
'''A minimal example of using simplebench.'''

import simplebench
from simplebench import benchmark


@benchmark
def addition_benchmark():
    '''A simple addition benchmark.'''
    sum(range(1000))


@benchmark('string_ops',
           title='String Concatenation Benchmark')
def string_concatenation_benchmark():
    '''A simple string concatenation benchmark.'''
    result = ''
    for i in range(1000):
        result += str(i)


if __name__ == '__main__':
    extra_args = ['--progress']
    simplebench.main(extra_args=extra_args)
