from uci_engine import Engine
import os
import platform


engine_path = "engines/"

win = platform.system() == 'Windows'
prefix = "" if win else "./"

print_fails = False

# Test template
def test(testfile, test_func):

    for engine_name in os.listdir(engine_path):

        engine = Engine(prefix + engine_name, engine_path)

        with open("testfiles/" + testfile, 'r') as fens:
            failures = 0
            for count, fen in enumerate(fens):
                print('\r[%4d] ' % (count+1), end='')
                if not test_func(engine, fen):
                    if print_fails:
                        print(fen, end='')
                    failures += 1

        result = "%d failures" % failures if failures else "success"

        print("\r%s test with %s of %s: %s" % (test_func.__name__, testfile, engine_name, result))


if __name__ == "__main__":
    test("all.epd", lambda x, y : True)
