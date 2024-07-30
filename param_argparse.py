#!/bin/python3

# python seu_script.py -f "texto exemplo" -b 123

import argparse

def main():
    # Cria um objeto ArgumentParser
    parser = argparse.ArgumentParser(description='Descrição do seu programa')

    # Define os argumentos que seu programa aceita
    parser.add_argument('-f', '--foo', type=str, help='Um argumento de exemplo')
    parser.add_argument('-b', '--bar', type=int, help='Outro argumento de exemplo')
    parser.add_argument('-v', '--verbose', action='store_true', help='Modo verbose')
    parser.add_argument('-f', '--file', type=str, required=True, help='Full Filename')
    parser.add_argument('-t', '--to', type=str, default='/tmp',  help='Path to')

    # Analisa os argumentos da linha de comando
    args = parser.parse_args()

    # Use os argumentos como desejar
    if args.foo:
        print(f"Argumento foo: {args.foo}")
    if args.bar:
        print(f"Argumento bar: {args.bar}")

if __name__ == "__main__":
    main()
