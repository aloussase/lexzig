from argparse import ArgumentParser

from sys import platform
if platform == "linux" or platform == "linux2":
    import readline

from rich.console import Console

from lexzig.parser import Parser, ParserError

REPL_BANNER = """Welcome to the LexZig repl!

Enter commands to see the result.
Enter 'q' to quit.
"""

console = Console()
error_console = Console(stderr=True)


def report_error(parser_error):
    if parser_error.lineno is not None:
        lineinfo = f"at line {parser_error.lineno}: "
    else:
        lineinfo = ""

    error_console.print(
        f"[bold red]ERROR:[/] {lineinfo}" +
        str(parser_error)
    )


def analyze_file(filename: str) -> None:
    parser = Parser()
    with open(filename) as f:
        try:
            console.print(parser.parse(f.read()))
        except ParserError as parser_error:
            report_error(parser_error)


def repl() -> None:
    parser = Parser()
    console.print(REPL_BANNER, style="bold")

    while (line := console.input(":high_voltage: ")) != 'q':
        try:
            result = parser.parse(line)
            console.print(result)
        except ParserError as parser_error:
            report_error(parser_error)


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
