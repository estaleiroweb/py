#!/bin/python3

# python seu_script.py -f "texto exemplo" -b 123

import getopt
import sys

def main():
    # Define os argumentos curtos e longos
    short_opts = "hf:b:"
    long_opts = ["help", "foo=", "bar="]

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("Ajuda")
            sys.exit()
        elif opt in ("-f", "--foo"):
            print(f"Argumento foo: {arg}")
        elif opt in ("-b", "--bar"):
            print(f"Argumento bar: {arg}")

if __name__ == "__main__":
    main()
