from subprocess import Popen, PIPE


# Interface for running and communicating with a UCI engine
class Engine:

    def __init__(self, path):
        self._process = Popen(path, shell=True, stdin=PIPE, stdout=PIPE, universal_newlines=True, bufsize=1)

    def _msg_engine(self, msg):
        self._process.stdin.write(msg)

    def _readline(self):
        return self._process.stdout.readline()

    def set_option(self, name, value):
        self._msg_engine("setoption name %s value %d\n" %(name, value))

    # Returns the evaluation relative to white pov
    def eval(self, fen):
        self._msg_engine("position fen " + fen + "\neval\n")
        return int(self._readline())
