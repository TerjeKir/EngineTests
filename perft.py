from uci_engine import Engine


# Tests whether the engine perft is correct
def perft(engine_path, test_path, depth):

    engine = Engine(engine_path)

    with open(test_path, 'r') as fens:
        failures = 0
        for count, fen in enumerate(fens):
            print('\r[%3d] ' % (count+1), end='')
            result = engine.perft(fen, depth)
            tokens = fen.split()
            solution = int(tokens[1 + tokens.index(";D%d" % depth)])
            if result != solution:
                print(fen, end='')
                failures += 1

    print("\rPerft test: %s" % ("%d wrong" % failures if failures else "success"))

if __name__ == "__main__":
    perft("weiss.exe", "EPDs/perftsuite.epd", 6)
