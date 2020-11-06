import chess
from uci_engine import Engine
from test import test


# Tests whether evaluation is symmetrical or not
# Relies on 'eval' command returning an evaluation from white p.o.v.
def eval_symmetry(engine_path, test_path):

    def symmetry_test(engine, fen):
        fen = ' '.join(fen.split()[:4])
        mirror_board = chess.Board()
        mirror_board.set_epd(fen)
        mirror_board = mirror_board.mirror()

        eval        =  engine.eval(fen)
        mirror_eval = -engine.eval(mirror_board.fen())

        return eval == mirror_eval

    test(engine_path, test_path, symmetry_test)

if __name__ == "__main__":
    eval_symmetry("weiss.exe", "EPDs/all.epd")
