# Original script by Koivisto dev Luecx

import os
import re
from uci_engine import Engine
from math import sqrt


# Config
depth = None
engine_dir = 'engines/'
engines = [engine for engine in os.listdir(engine_dir)]


class Result:
    def __init__(self):
        self.benches = []

    def add_bench(self, bench):
        self.benches.append(bench)

    def compute_mu(self):
        if len(self.benches) < 1:
            return 0
        return sum(self.benches) / len(self.benches)

    def compute_sigma_squared(self):
        if len(self.benches) < 2:
            return 0
        mu = self.compute_mu()
        return 1.0 / (len(self.benches) - 1) * sum((x - mu) ** 2 for x in self.benches)

    def compute_sigma(self):
        return sqrt(self.compute_sigma_squared())

def show_header(names):
    print(''.join(f'{name : ^36}|' for name in names))
    print(''.join(f'{"mu" : ^18}{"sigma" : ^18}|' for _ in names) + \
          f'{"Sp(1)/Sp(2)" : ^18}{"3*sigma" : ^12}')
    print('+'.join('------------------------------------' for _ in range(len(names) + 1)))

def show(results, comparison):
    for r in results:
        print(f'{r.compute_mu() : 18.3f}{r.compute_sigma() : 18.3f}|', end='')

    print(f'{100 * comparison.compute_mu()   : 12.3f} %  +/- ' + \
          f'{300 * comparison.compute_sigma() : 6.3f} %')


# Regex matching number followed by '(optional whitespace)nps'
nps_matcher = re.compile(r'\d+(?=\s*nps)')

show_header(engines)

results = [Result() for _ in engines]
comparison = Result()
try: # No stack trace when interrupted
    while True:
        for i, bench in enumerate(Engine.bench(engine, depth, engine_dir) for engine in engines):
            for line in reversed(bench.split('\n')):
                nps = re.search(nps_matcher, line)
                if (nps == None): continue
                results[i].add_bench(int(nps[0]))
                break
            else:
                print("Didn't find bench nps.")
                quit()

        # compute a relative speed difference
        comparison.add_bench(results[0].benches[-1] / results[1].benches[-1] - 1.0)

        show(results, comparison)
except:
    quit(0)
