import chess.pgn
from random import sample


dataset = "datasets/tuning_games0.pgn"
output = "datasets/samples.epd"

samples_per_game = 10


def sample_pgn():
    with open(dataset, 'r') as pgn, open(output, 'w') as out:
        while True:
            game = chess.pgn.read_game(pgn)
            if not game:
                break
            result = game.headers["Result"]
            game_length = int(game.headers["PlyCount"])
            board = game.board()
            samples = sample(range(game_length), min(samples_per_game, game_length))
            for ply, move in enumerate(game.mainline_moves()):
                board.push(move)
                if ply in samples and not board.is_checkmate():
                    print(board.fen() + " [%s]" % result, file=out)


if __name__ == "__main__":
    sample_pgn()
