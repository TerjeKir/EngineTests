from subprocess import Popen, PIPE
import platform


startpos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

win = platform.system() == 'Windows'
prefix = "" if win else "./"


# Interface for running and communicating with a UCI engine
class Engine:

    def __init__(self, path, cwd=None):
        _prefix = "java -jar " if "jar" in path else prefix
        self._process = Popen(_prefix + path, shell=True, cwd=cwd, stdin=PIPE, stdout=PIPE, universal_newlines=True, bufsize=1)
        self.uci()
        self.set_option("Threads", 1)
        self.set_option("Hash", 32)
        self.isready()

    def _msg_engine(self, msg):
        self._process.stdin.write(msg)

    def _readline(self):
        return self._process.stdout.readline()


    ### UCI commands

    def uci(self):
        self._msg_engine("uci\n")
        while True:
            if self._readline() == "uciok\n":
                break

    def ucinewgame(self):
        self._msg_engine("ucinewgame\n")

    def isready(self):
        self._msg_engine("isready\n")
        while True:
            if self._readline() == "readyok\n":
                break

    def stop(self):
        self._msg_engine("stop\n")

    def quit(self):
        self._msg_engine("quit\n")

    def set_option(self, name, value):
        self._msg_engine(f"setoption name {name} value {value}\n")

    def position(self, fen=startpos, moves=None):
        moves = f" moves {moves}" if moves else ""
        self._msg_engine(f"position fen {fen}{moves}\n")

    # limitstring can be used to provide limits not supported by other arguments
    def go(self, mate=None, movetime=None, depth=None, limitstring=""):
        limits = ' '.join(f"{key} {value}" for key, value in locals().items() if key not in ("self", "limitstring") and value)
        limits += f" {limitstring}" if limitstring else ""
        self._msg_engine(f"go {limits}\n")


    ### Non-UCI commands

    ## 'eval'
    # The engine should respond with an evaluation from white's point of view
    def eval(self, fen):
        self.position(fen)
        self._msg_engine("eval\n")
        return int(self._readline())

    ## 'perft <depth> <fen>' or just 'perft <depth>' after a position command
    # The engine should print the perft count as a line with a single integer or
    # as part of a string where it is the first digit after 'nodes'/'nodes:' etc
    def perft(self, fen, depth):
        self.isready()
        self.position(fen)
        self._msg_engine(f"perft {depth} {fen}\n")
        while True:
            response = self._readline().lower()
            # A line with just a single number should be the perft count
            if response.strip().isdigit():
                return int(response)
            # A line with 'nodes' should have the perft count as the first subsequent number
            if 'nodes' in response:
                for token in response.split('nodes')[1].split():
                    if token.isdigit():
                        return int(token)
