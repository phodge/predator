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
    from predator.common import GrammarConstructionError
    from predator.grammar import Regex

    # things that do work
    a_dot = Regex('a_dot', '.')
    assert a_dot.item_name == 'a_dot'

    nn = Regex(None, '(?:regex with no name)')
    assert nn.item_name is None

    # things that won't work
    things_that_fail = (
        # empty regex
        '',
        # something that isn't a valid regex
        '*',
    )

    for badinput in things_that_fail:
        try:
            # symbols don't work
            Regex(None, badinput)
        except GrammarConstructionError:
            pass
        else:
            err = 'Regex(None, {!r}) should have failed'.format(badinput)
            raise Exception(err)

    # make sure Literal has a nice repr
    _checkrepr(Regex('many_As', 'A+'), ['many_As', 'A+'])


def test_construct_linebreak():
    from predator.grammar import Linebreak
    # it takes no arguments
    Linebreak()
    # there's nothing exciting in the repr
    _checkrepr(Linebreak(), [])


def test_construct_choice():
    from predator.grammar import Choice, Word

    # you may give your Choice a name
    c1 = Choice('person_names')
    c1.addchoice(Word('fred'))
    c1.addchoice(Word('john'))
    c1.addchoice(Word('bill'))

    # you can also have a Choice without a name
    c2 = Choice(None)
    c2.addchoice(Word('aaa'))
    c2.addchoice(Word('bbb'))


def test_construct_sequence():
    from predator.grammar import Literal, Sequence, Word

    # you can construct a sequence and tell it to match things in sequence
    s = Sequence(None)
    s.additem(Word('a'))
    s.additem(Word('b'))
    s.additem(Word('c'))

    # you can give it a name and tell it to ignore spaces
    s = Sequence('hashbang', spaces=False)
    s.additem(Literal('#'))
    s.additem(Literal('!'))

    # you can give the children names
    s = Sequence(None)
    s.additem(Literal('#'), 'hash')
    s.additem(Literal('!'), 'bang')

    # you can make the children repeat or be optional
    s = Sequence(None, spaces=False)
    s.additem(Literal('#'), many=True)
    s.additem(Literal('!'), optional=True)


def test_construct_whitespace():
    from predator.grammar import (Literal, Linebreak, Regex, Sequence,
                                  Whitespace, Word, Choice)

    # you can construct a whitespace sequence manually
    w = Whitespace()
    assert w.is_white

    # and then you can add normal items to it
    w.addwhitespaceitem(Literal('.'))
    w.addwhitespaceitem(Literal('"'))
    w.addwhitespaceitem(Linebreak())
    w.addwhitespaceitem(Word('rem'))
    # NOTE: this is a poor Regex example because it can't cross linebreaks
    w.addwhitespaceitem(Regex('c_style_comment', r'/\*.*\*/'))

    # you can even add complex sequences as children
    s = Sequence('c_style_comment_2')
    s.additem(Literal('/*'))
    s.additem(Regex('c_style_comment_inside', r'(\*[^/]|[^*])*'))
    s.additem(Literal('*/'))
    assert not hasattr(s, 'is_white')
    w.addwhitespaceitem(s)
    assert s.is_white is True

    # you can add your whitespace item to another whitespace item
    w2 = Whitespace()
    w2.addwhitespaceitem(w)
    del w, s, w2

    # recursive patterns are allowed
    w1 = Sequence('white_one')
    w2 = Choice('white_two')
    w1.additem(Word('one'))
    w1.additem(w2)
    w2.addchoice(w1)
    w2.addchoice(Word('two'))

    # adding the items to the Whitespace() item turns them into whitespace also
    assert not hasattr(w1, 'is_white')
    assert not hasattr(w2, 'is_white')
    w3 = Whitespace()
    w3.addwhitespaceitem(w1)
    w3.addwhitespaceitem(w2)
    assert w1.is_white and w2.is_white


def _checkrepr(item, lookfor):
    """
    Checks that a grammar item's repr() is sane.
    """
    r = repr(item)
    assert r.startswith('<') and r.endswith('>')
    assert item.__class__.__name__ in r
    for text in lookfor:
        assert text in r
