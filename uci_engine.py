from subprocess import Popen, PIPE
import platform


startpos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

win = platform.system() == 'Windows'
prefix = "" if win else "./"


# Interface for running and communicating with a UCI engine
class Engine:

    def __init__(self, name, path=None, noinit=False):
        _prefix = "java -jar " if "jar" in name else prefix
        self._process = Popen(_prefix + name, shell=True, cwd=path, stdin=PIPE, stdout=PIPE, universal_newlines=True, bufsize=1)
        if noinit: return
        self.uci()
        self.set_option("Threads", 1)
        self.set_option("Hash", 32)
        self.isready()

    def writeline(self, msg):
        self._process.stdin.write(msg)

    def readline(self):
        return self._process.stdout.readline().rstrip()


    ### UCI commands

    def uci(self):
        self.writeline("uci\n")
        while self.readline() != "uciok": pass

    def ucinewgame(self):
        self.writeline("ucinewgame\n")

    def isready(self):
        self.writeline("isready\n")
        while self.readline() != "readyok": pass

    def stop(self):
        self.writeline("stop\n")

    def quit(self):
        self.writeline("quit\n")

    def set_option(self, name, value):
        self.writeline(f"setoption name {name} value {value}\n")

    def position(self, fen=startpos, moves=None):
        moves = f" moves {moves}" if moves else ""
        self.writeline(f"position fen {fen}{moves}\n")

    # limitstring can be used to provide limits not supported by other arguments
    def go(self, **limits):
        limits = ' '.join(f"{key} {value}" for key, value in limits.items())
        self.writeline(f"go {limits}\n")


    ### Non-UCI commands

    ## 'eval'
    # The engine should respond with an evaluation from white's point of view
    def eval(self, fen):
        self.position(fen)
        self.writeline("eval\n")
        return int(self.readline())

    ## 'perft <depth> <fen>' or just 'perft <depth>' after a position command
    # The engine should print the perft count as a line with a single integer or
    # as part of a string where it is the first digit after 'nodes'/'nodes:' etc
    def perft(self, fen, depth):
        self.isready()
        self.position(fen)
        self.writeline(f"perft {depth} {fen}\n")
        while True:
            response = self.readline().lower()
            # A line with just a single number should be the perft count
            if response.isdigit():
                return int(response)
            # A line with 'nodes' should have the perft count as the first subsequent number
            if 'nodes' in response:
                for token in response.split('nodes')[1].split():
                    if token.isdigit():
                        return int(token)

    def bench(name, depth=None, path=None):
        engine = Engine(f"{name} bench {depth if (depth) else ''}", path=path, noinit=True)
        bench, _ = engine._process.communicate()
        return bench
