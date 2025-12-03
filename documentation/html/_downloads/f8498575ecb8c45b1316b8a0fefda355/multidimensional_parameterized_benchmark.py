"""A multidimensional parameterized benchmark."""
import simplebench


@simplebench.benchmark(
        kwargs_variations={
            'size': [10, 100, 1000],
            'mode': ['fast', 'slow']
        },
        variation_cols={
            'size': 'Input Size',
            'mode': 'Mode'
        },
        use_field_for_n='size')
def my_benchmark(size: int, mode: str) -> None:
    """A benchmark for summing a range of numbers that varies by size and mode."""
    match mode:
        case 'fast':
            sum(range(size))
        case 'slow':
            total = 0
            for i in range(size):
                total += i


if __name__ == "__main__":
    simplebench.main()
