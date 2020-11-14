import chess
from test import test


# Tests whether evaluation is symmetrical or not
# Relies on 'eval' command returning an evaluation from white p.o.v.
def eval_symmetry(testfile):

    def symmetry(engine, fen):
        fen = ' '.join(fen.split()[:4])
        board = chess.Board()
        board.set_epd(fen)
        mirror_board = board.mirror()

        eval        =  engine.eval(fen)
        mirror_eval = -engine.eval(mirror_board.fen())

        return eval == mirror_eval

    test(testfile, symmetry)


if __name__ == "__main__":
    eval_symmetry("all.epd")
