from test import test


# Tests whether the engine finds a short enough mate within the time limit
def mate_test(testfile, length, limit_in_ms):

    def mate(engine, fen):
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

    test(testfile, mate)


if __name__ == "__main__":
    for depth in range(1, 9):
        for color in ('w', 'b'):
            mate_test("mate%d-%s.epd" % (depth, color), depth, 1000)
