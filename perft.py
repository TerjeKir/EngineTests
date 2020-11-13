from test import test


# Tests whether the engine perft is correct
def perft_test(test_path, depth):

    def perft(engine, fen):
        result = engine.perft(fen, depth)
        tokens = fen.split()
        solution = int(tokens[1 + tokens.index(";D%d" % depth)])

        return result == solution

    test(test_path, perft)


if __name__ == "__main__":
    perft_test("EPDs/perftsuite.epd", 4)
