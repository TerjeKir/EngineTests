from uci_engine import Engine
import os


engine_path = "engines/"

# Test template
def test(testfile, test_func, print_fails):

    for engine_name in os.listdir(engine_path):

        engine = Engine(engine_name, engine_path)

        with open(f"testfiles/{testfile}", 'r') as fens:
            fail_count = 0
            for count, fen in enumerate(fens):
                print(f"\r[{count+1:4d}] ", end='')
                if not test_func(engine, fen):
                    if print_fails:
                        print(fen, end='')
                    fail_count += 1

        result = f"{fail_count} failures" if fail_count else "success"

        print(f"\r{test_func.__name__} test with {testfile} of {engine_name}: {result}")


if __name__ == "__main__":
    test("all.epd", lambda x, y : True)
