import chess.pgn
from random import sample


dataset = "datasets/tuning_games0.pgn"
output = "datasets/samples.epd"

samples_per_game = 10


class Visitor(chess.pgn.BaseVisitor):
    def begin_game(self):
        self.fens = []
        self.gameresult = ""
        self.relevant = True

    def visit_header(self, name, value):
        if name == "Termination" and value != "adjudication":
            self.relevant = False
        if name == "Result":
            self.gameresult = value

    def end_headers(self):
        if not self.relevant:
            # Optimization hint: Do not even bother parsing the moves.
            return chess.pgn.SKIP

    # Will also be called for the terminal position of the game.
    # Keep using visit_move instead, if that's not desired.
    def visit_board(self, board):
        if self.relevant:
            self.fens.append(board.fen())

    def result(self):
        return self.gameresult, self.fens


def sample_pgn():
    with open(dataset, 'r') as pgn, open(output, 'w') as out:
        while True:
            result, fens = chess.pgn.read_game(pgn, Visitor=Visitor)
            if not fens:
                break
            for fen in sample(fens, min(samples_per_game, len(fens))):
                print(fen + " [%s]" % result, file=out)


if __name__ == "__main__":
    sample_pgn()
