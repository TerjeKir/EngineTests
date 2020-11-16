from subprocess import Popen, PIPE
import platform


startpos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

win = platform.system() == 'Windows'
prefix = "" if win else "./"


# Interface for running and communicating with a UCI engine
class Engine:

    def __init__(self, path, cwd=None):
        self._process = Popen(prefix + path, shell=True, cwd=cwd, stdin=PIPE, stdout=PIPE, universal_newlines=True, bufsize=1)
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
        self._msg_engine("setoption name %s value %d\n" %(name, value))

    def position(self, fen=startpos, moves=None):
        self._msg_engine("position fen %s%s\n" % (fen, " moves %s" % moves if moves else ""))

    # limitstring can be used to provide limits not supported by other arguments
    def go(self, mate=None, movetime=None, depth=None, limitstring=""):
        for key, value in locals().items():
            if key not in ("self", "limitstring") and value:
                limitstring += " %s %d" % (key, value)
        self._msg_engine("go %s\n" % limitstring)


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
        self.position(fen)
        self._msg_engine("perft %d %s\n" % (depth, fen))
        while True:
            response = self._readline().lower()
            # A line with just a single number should be the perft count
            if response.isdigit():
                return int(response)
            # A line with 'nodes' should have the perft count as the first subsequent number
            if 'nodes' in response:
                for token in response.split('nodes')[1].split():
                    if token.isdigit():
                        return int(token)

engine = Engine("weiss.exe", "engines/")
engine.go(mate = 5, movetime = 1000, depth = 8, limitstring="infinite")
engine.go(mate = 5, depth = 8)
