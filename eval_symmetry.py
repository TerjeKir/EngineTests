import chess
from uci_engine import Engine


# Tests whether evaluation is symmetrical or not
# Relies on 'eval' command returning an evaluation from white p.o.v.
def eval_symmetry(engine_path, fen_path):

    engine = Engine(engine_path)
    mirror_board = chess.Board()

    with open(fen_path, 'r') as fens:
        for count, fen in enumerate(fens):
            fen = ' '.join(fen.split()[:4])
            mirror_board.set_epd(fen)
            mirror_board = mirror_board.mirror()

            eval        =  engine.eval(fen)
            mirror_eval = -engine.eval(mirror_board.fen())

            if eval != mirror_eval:
                return print("Eval symmetry test: fail")

            if count % 1000 == 0:
                print(count, end='\r')

        print("Eval symmetry test: success")

if __name__ == "__main__":
    eval_symmetry("weiss.exe", "EPDs/all.epd")
