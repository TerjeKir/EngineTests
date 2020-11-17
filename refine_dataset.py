from uci_engine import Engine
import chess


dataset = "datasets/samples.epd"
output = "datasets/refined.epd"

engine_path = "engines/"
engine_name = "weiss.exe"

filter_limit = 1000


def refine():

    engine = Engine(engine_name, engine_path)

    with open(dataset, 'r') as fens, open(output, 'w') as out:
        for fen in fens:
            ## Do an x depth search and save the final given pv
            fen = ' '.join(fen.split()[:4]) + " 0 1"
            engine.position(fen)
            engine.go(depth=6)

            while True:
                response = engine._readline()
                if "bestmove" in response:
                    break
                final_info = response

            # Filter out positions where score is too high or mate
            tokens = final_info.split()
            score = int(tokens[2 + tokens.index("score")])
            is_mate = "mate" in tokens

            if is_mate or abs(score) > filter_limit:
                continue

            pv = final_info.split("pv ")[1].split()

            ## Follow the pv and save the final fen
            board = chess.Board(fen)
            for move in pv:
                board.push_uci(move)

            print(board.fen(), file=out)


if __name__ == "__main__":
    refine()
