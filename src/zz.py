import sys

import constant
import program


# TODO: Needs argument handling
def main(argv):
    program.run(argv[1])


# Entry point
if __name__ == '__main__':
    main(sys.argv)
