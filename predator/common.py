"""
Errors and miscellaneous utilities.
"""
import re

LINEBREAK_RE = re.compile(r'\r\n?|\n')


class GrammarConstructionError(Exception):
    """
    Raised when something attempts to create an instance of a
    predator.grammar.Item subclass using bad arguments.
    """
