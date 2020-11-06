from uci_engine import Engine
from test import test


# Tests whether the engine perft is correct
def perft(engine_path, test_path, depth):

    def test_perft(engine, fen):
        result = engine.perft(fen, depth)
        tokens = fen.split()
        solution = int(tokens[1 + tokens.index(";D%d" % depth)])
        return result == solution

    test(engine_path, test_path, test_perft)

if __name__ == "__main__":
    perft("weiss.exe", "EPDs/perftsuite.epd", 4)
