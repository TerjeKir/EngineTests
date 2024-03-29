from test import test


print_fails = True

# Tests whether the engine perft is correct
def perft_test(testfile, depth):

    def perft(engine, fen):
        result = engine.perft(fen, depth)
        tokens = fen.split()
        solution = int(tokens[1 + tokens.index(f";D{depth}")])

        return result == solution

    test(testfile, perft, print_fails)


if __name__ == "__main__":
    perft_test("perftsuite.epd", 5)
