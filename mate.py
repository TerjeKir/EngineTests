import chess
from uci_engine import Engine
from test import test


# Tests whether the engine finds a short enough mate within the time limit
def mate_test(engine_path, test_path, length, limit_in_ms):

    def find_mate(engine, fen):
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

    test(engine_path, test_path, find_mate)


if __name__ == "__main__":
    mate_test("weiss.exe", "EPDs/mate3-w.epd", 3, 1000)
