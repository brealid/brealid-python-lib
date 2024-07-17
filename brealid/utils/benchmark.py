import time
from tqdm.auto import tqdm
from .calc import mean, std

def fmtTime(duration):
    if duration >= 1:
        return f"{duration:.3g}"
    elif duration >= 1e-3:
        return f"{duration * 1e3:.3g}ms"
    elif duration >= 1e-6:
        return f"{duration * 1e6:.3g}µs"
    else:
        return f"{duration * 1e9:.3g}ns"
    
def fmtBig(bignum):
    return f"{bignum:.3g}"
    if bignum >= 1000**3:
        return f"{bignum/1000**3:.3g}G"
    elif bignum >= 1000**2:
        return f"{bignum/1000**2:.3g}M"
    elif bignum >= 1000**1:
        return f"{bignum/1000**1:.3g}K"
    else:
        return f"{bignum:.3g}"

def time_the_func(to_measure):
    def __wrapper__(*args, **kwargs):
        start = time.time()
        to_measure(*args, **kwargs)
        return time.time() - start
    return __wrapper__

@time_the_func
def empty_looping(n, m):
    for i in range(1, n+1):
        [0 for j in range(1, m+1)]

@time_the_func
def adding(n, m):
    for i in range(1, n+1):
        [i + j for j in range(1, m+1)]

@time_the_func
def multiple(n, m):
    for i in range(1, n+1):
        [i * j for j in range(1, m+1)]

@time_the_func
def float_dividing(n, m):
    for i in range(1, n+1):
        [i / j for j in range(1, m+1)]

def benchmark(n = 10000, m = 10000):
    print('[Note] this benchmark based on python and isn\'t stable')
    
    # Empty Looping
    timing = []
    with tqdm(range(7), leave=False) as bar:
        for i in bar:
            timing.append(empty_looping(n, m))
    timing = [t / (n * m) for t in timing]
    _mean, _std = mean(timing), std(timing)
    print(f'[+] {fmtTime(_mean)} ± {fmtTime(_std)} per operation (mean ± std. dev. of 7 runs, {n * m:,} loops each)')
    print(f'    Empty Looping ==> {fmtBig(1 / _mean)}/s')
    mean_empty_looping = _mean
    
    # Adding
    timing = []
    with tqdm(range(7), leave=False) as bar:
        for i in bar:
            timing.append(adding(n, m) - mean_empty_looping)
    timing = [t / (n * m) for t in timing]
    _mean, _std = mean(timing), std(timing)
    print(f'[+] {fmtTime(_mean)} ± {fmtTime(_std)} per operation (mean ± std. dev. of 7 runs, {n * m:,} loops each)')
    print(f'    Adding ==> {fmtBig(1 / _mean)}/s')
    
    # Multiple
    timing = []
    with tqdm(range(7), leave=False) as bar:
        for i in bar:
            timing.append(multiple(n, m) - mean_empty_looping)
    timing = [t / (n * m) for t in timing]
    _mean, _std = mean(timing), std(timing)
    print(f'[+] {fmtTime(_mean)} ± {fmtTime(_std)} per operation (mean ± std. dev. of 7 runs, {n * m:,} loops each)')
    print(f'    Multiple ==> {fmtBig(1 / _mean)}/s')
    
    # Float Dividing
    timing = []
    with tqdm(range(7), leave=False) as bar:
        for i in bar:
            timing.append(float_dividing(n, m) - mean_empty_looping)
    timing = [t / (n * m) for t in timing]
    _mean, _std = mean(timing), std(timing)
    print(f'[+] {fmtTime(_mean)} ± {fmtTime(_std)} per operation (mean ± std. dev. of 7 runs, {n * m:,} loops each)')
    print(f'    Float Dividing ==> {fmtBig(1 / _mean)}/s')
    
benchmark(2000, 10000)