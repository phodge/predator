from predator.grammar.common import Item


class Choice(Item):
    """
    A grammar object that attempts to match text using one of several other
    grammar Items.
    """
