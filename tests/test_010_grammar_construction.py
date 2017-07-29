"""
The follow tests are designed to prove that you can _construct_ a tree of
grammar items using the predator.grammar.Item subclasses.
"""


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
    assert False, 'Test is unfinished'


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
