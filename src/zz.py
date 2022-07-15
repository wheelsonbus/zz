import sys

from constant import *
from program import *


# TODO: Needs argument handling
def main(argv):
    program = Program(argv[1])
    program.run()


# Entry point
if __name__ == '__main__':
    main(sys.argv)
