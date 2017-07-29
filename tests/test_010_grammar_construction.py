"""
The follow tests are designed to prove that you can _construct_ a tree of
grammar items using the predator.grammar.Item subclasses.
"""


def test_item():
    from predator.common import GrammarConstructionError
    from predator.grammar import Item

    # items can be constructed with no name
    i = Item(None)
    assert i.item_name is None

    # items can be constructed with a name
    i = Item('my_cool_item')
    assert i.item_name == 'my_cool_item'

    # some bad names that won't work
    things_that_fail = (
        # empty names
        '',
        # names that don't match WORD_RE
        ' ',
        '!bang',
        ' wheeee',
    )
    for badname in things_that_fail:
        try:
            Item(badname)
        except GrammarConstructionError:
            pass
        else:
            err = 'Item name {!r} should have failed'.format(badname)
            raise Exception(err)


def test_construct_word():
    from predator.common import GrammarConstructionError
    from predator.grammar import Word

    # things that do work
    Word('hello')
    Word('a')
    Word('AVeryLongWordThatWillAlsoWork')
    Word('L3375p34k')

    # things that won't work
    things_that_fail = (
        'multiple words',
        'multiple\nlines',
        # can't be wrapped in whitespace
        ' hello',
        'hello ',
        # symbols aren't allowed
        '!@#$',
        # not even in the middle of a word
        'he!!o',
        # words can't start with a digit
        '5hello',
        # also can't be empty
        '',
        ' ',
    )

    for badword in things_that_fail:
        try:
            # symbols don't work
            Word(badword)
        except GrammarConstructionError:
            pass
        else:
            raise Exception('Word({!r}) should have failed'.format(badword))

    # make sure Word has a nice repr
    _checkrepr(Word('hello'), ['hello'])


def test_construct_literal():
    from predator.common import GrammarConstructionError
    from predator.grammar import Literal

    # things that do work
    Literal(' ')
    Literal('!')
    Literal('@#')
    Literal('!@#$%^&*()_+')

    # they should accept names as well
    l = Literal('@', name='at_symbol')
    assert l.item_name == 'at_symbol'

    #FIXME: work out whether we should (or can) support NULs in our strings

    # things that won't work
    things_that_fail = (
        '\n',
        '!\n!',
        '\r',
        '!\r!',
        '',
    )

    for badinput in things_that_fail:
        try:
            # symbols don't work
            Literal(badinput)
        except GrammarConstructionError:
            pass
        else:
            err = 'Literal({!r}) should have failed'.format(badinput)
            raise Exception(err)

    # make sure Literal has a nice repr
    _checkrepr(Literal('%'), ['%'])
    _checkrepr(Literal('%', name='percent_sign'), ['%', 'percent_sign'])


def test_construct_regex():
    assert False, 'Test is unfinished'


def test_construct_linebreak():
    assert False, 'Test is unfinished'


def test_construct_choice():
    assert False, 'Test is unfinished'


def test_construct_sequence():
    assert False, 'Test is unfinished'


def test_construct_whitespace():
    assert False, 'Test is unfinished'


def test_construct_everything():
    assert False, 'Test is unfinished'


def _checkrepr(item, lookfor):
    """
    Checks that a grammar item's repr() is sane.
    """
    r = repr(item)
    assert r.startswith('<') and r.endswith('>')
    assert item.__class__.__name__ in r
    for text in lookfor:
        assert text in r
