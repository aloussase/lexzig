from argparse import ArgumentParser
import readline  # For readline support with rich

from rich.console import Console

from lexzig.parser import Parser


REPL_BANNER = """Welcome to the LexZig repl!

Enter commands to see the result.
Enter 'q' to quit.
"""

console = Console()
error_console = Console(stderr=True)


def analyze_file(filename: str) -> None:
    parser = Parser()
    with open(filename) as f:
        print(parser.parse(f.read()))


def repl() -> None:
    parser = Parser()
    console.print(REPL_BANNER, style="bold")

    while (line := console.input(":high_voltage: ")) != 'q':
        result = parser.parse(line)
        print(result)


def main() -> None:
    parser = ArgumentParser(
        prog='LexZig',
        description='Lexical and syntactical analysis for a subset of the Zig programming language.',
    )

    parser.add_argument('filename', help='The file to analyze.', nargs='?')
    parser.add_argument(
        '--repl', help='Start the repl. This is the default if not filename is provided.', action='store_true')

    args = parser.parse_args()

    if args.filename:
        analyze_file(args.filename)
    else:
        repl()


if __name__ == '__main__':
    main()
