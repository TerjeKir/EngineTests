# Original script by Koivisto dev Luecx

from uci_engine import Engine
import os, re
import matplotlib.pyplot as plt


# Config
maxthreads = 4
hash       = 128
movetime   = 5000
engine_dir = 'engines/'
engines    = [engine for engine in os.listdir(engine_dir)]

# positions  = ["r3k2r/2pb1ppp/2pp1q2/p7/1nP1B3/1P2P3/P2N1PPP/R2QK2R w KQkq a6 0 14",
#               "4rrk1/2p1b1p1/p1p3q1/4p3/2P2n1p/1P1NR2P/PB3PP1/3R1QK1 b - - 2 24",
#               "r3qbrk/6p1/2b2pPp/p3pP1Q/PpPpP2P/3P1B2/2PB3K/R5R1 w - - 16 42",
#               "6k1/1R3p2/6p1/2Bp3p/3P2q1/P7/1P2rQ1K/5R2 b - - 4 44",
#               "8/8/1p2k1p1/3p3p/1p1P1P1P/1P2PK2/8/8 w - - 3 54",
#               "7r/2p3k1/1p1p1qp1/1P1Bp3/p1P2r1P/P7/4R3/Q4RK1 w - - 0 36",
#               "r1bq1rk1/pp2b1pp/n1pp1n2/3P1p2/2P1p3/2N1P2N/PP2BPPP/R1BQ1RK1 b - - 2 10",
#               "3r3k/2r4p/1p1b3q/p4P2/P2Pp3/1B2P3/3BQ1RP/6K1 w - - 3 87",
#               "2r4r/1p4k1/1Pnp4/3Qb1pq/8/4BpPp/5P2/2RR1BK1 w - - 0 42",
#               "4q1bk/6b1/7p/p1p4p/PNPpP2P/KN4P1/3Q4/4R3 b - - 0 37"]

positions = ["r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"]

# Matches a number preceded by 'nps '
nps_matcher = re.compile(r'(?<=nps )\d+')
thread_range = range(1, maxthreads+1)
speeds = {}

for name in engines:

    speeds[name] = []
    engine = Engine(name, engine_dir)
    engine.set_option('Hash', hash)
    print(f'\n{name}')

    for threads in thread_range:

        engine.set_option('Threads', threads)
        total_nps = 0

        for position in positions:

            engine.ucinewgame()
            engine.position(position)
            engine.isready()
            engine.go(movetime=movetime)

            while True:
                l = engine.readline()
                if l.startswith('bestmove'):
                    break
                line = l

            total_nps += int(re.search(nps_matcher, line)[0])

        nps = int(total_nps / len(positions))
        speeds[name].append(nps)
        print(f'{threads}: {nps : >9} ({nps / speeds[name][0]: 5.2f})')


plt.grid()
plt.plot(thread_range, thread_range)

for engine in engines:
    base = speeds[engine][0]
    plt.plot(thread_range, [x / base for x in speeds[engine]], label=f"{engine} base: {base}")

plt.legend(loc='best')
plt.show()
