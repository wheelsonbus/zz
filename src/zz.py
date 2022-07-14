import sys

import constant
import program


# TODO: Needs argument handling
def main(argv):
    p = program.Program(argv[1])
    p.run()


# Entry point
if __name__ == '__main__':
    main(sys.argv)
