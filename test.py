from uci_engine import Engine


# Test template
def test(engine_path, test_path, test_func):

    engine = Engine(engine_path)

    with open(test_path, 'r') as fens:
        failures = 0
        for count, fen in enumerate(fens):
            print('\r[%4d] ' % (count+1), end='')
            if not test_func(engine, fen):
                print(fen, end='')
                failures += 1

    print("\rTest: %s" % ("%d failures" % failures if failures else "success"))


if __name__ == "__main__":
    test("weiss.exe", "EPDs/mate3-w.epd", lambda x, y : True)
