"""
Errors and miscellaneous utilities.
"""
import re

LINEBREAK_RE = re.compile(r'\r\n?|\n')
WORD_RE = re.compile(r'[A-Za-z_][A-Za-z_0-9]*')


class GrammarConstructionError(Exception):
    """
    Raised when something attempts to create an instance of a
    predator.grammar.Item subclass using bad arguments.
    """
