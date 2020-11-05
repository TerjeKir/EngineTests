import chess
from uci_engine import Engine


# Tests whether the engine finds a short enough mate within the time limit
def mate_test(engine_path, test_path, length, limit_in_ms):

    engine = Engine(engine_path)

    def find_mate(fen):
        engine.ucinewgame()
        engine.position(fen)
        engine.go(mate=length, movetime=limit_in_ms)
        mate_found = False

        while True:
            response = engine._readline()
            mate_found |= "mate %d" % length in response
            if response.startswith('bestmove'):
                break

        return mate_found


    with open(test_path, 'r') as fens:
        failures = 0
        for count, fen in enumerate(fens):
            print('\r[%4d] ' % (count+1), end='')
            if not find_mate(fen):
                print(fen, end='')
                failures += 1

    print("\rMate test: %s" % ("%d unsolved" % failures if failures else "success"))


if __name__ == "__main__":
    mate_test("weiss.exe", "EPDs/mate3-w.epd", 3, 1000)
