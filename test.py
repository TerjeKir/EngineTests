from uci_engine import Engine
import os


engine_path = "engines/"

# Test template
def test(filename, test_func):

    for engine_name in os.listdir(engine_path):

        engine = Engine(engine_name, engine_path)

        with open("testfiles/" + filename, 'r') as fens:
            failures = 0
            for count, fen in enumerate(fens):
                print('\r[%4d] ' % (count+1), end='')
                if not test_func(engine, fen):
                    print(fen, end='')
                    failures += 1

        result = "%d failures" % failures if failures else "success"

        print("\r%s test of %s: %s" % (test_func.__name__, engine_name, result))


if __name__ == "__main__":
    test("mate3-w.epd", lambda x, y : True)
