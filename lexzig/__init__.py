import lexzig.ast as ast
from lexzig.parser import Parser


def run_analysis(input: str) -> ast.Program:
    """
    Analyse the given source code.
    """
    return Parser().parse(input)
