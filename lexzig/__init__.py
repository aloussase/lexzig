from ply.lex import LexToken  # type: ignore

from typing import Tuple, List

import lexzig.ast as ast
from lexzig.parser import Parser
from lexzig.lexer import Lexer


def run_analysis(input: str) -> Tuple[List[LexToken], ast.Program]:
    """
    Analyse the given source code.
    """
    return Lexer().lex(input), Parser().parse(input)
