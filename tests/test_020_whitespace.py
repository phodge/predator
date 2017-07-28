import pytest  # noqa


def _get_grammar():
    from predator.grammar import Sequence, Whitespace, Word

    message = Sequence("message", spaces=True)
    message.additem(Word("hello"), "the_hello")
    message.additem(Word("reee"), "the_reee")
    message.additem(Word("goodbye"), "the_goodbye")
    message.initleader(Whitespace())


def asserttip(node_, txt, *, name=None, where):
    from predator.nodes import Tip

    assert isinstance(node_, Tip)
    assert node_.node_text == txt
    if name is None:
        assert node_.node_name is None
    else:
        assert node_.node_name == name
    assert node_.line_start == where[0]
    assert node_.line_end == where[0]
    assert node_.char_start == where[1]
    assert node_.char_end == where[1] + len(txt) - 1


def parsenow(item, data):
    from predator.io import InputStream
    from predator.nodes import Fork

    first, gen = item.parseall(InputStream(data))

    if first is not None:
        assert isinstance(first, Fork)
        assert not len(first.getfaults())
        return first

    second = gen.send(None)
    assert len(second.getfaults())
    for f in second.getfaults():
        import pprint
        print('f = ' + pprint.pformat(f))  # noqa TODO
    raise Exception("parsenow() returned a faulty node")


def test_linebreaks():
    message = _get_grammar()

    data = "hello\nreee\n\ngoodbye"
    first = parsenow(message, data)
    asserttip(first['the_hello'],   "hello",   where=(1, 0))
    asserttip(first["the_reee"],    "reee",    where=(2, 0))
    asserttip(first['the_goodbye'], "goodbye", where=(4, 0))


def test_spaces_and_tabs():
    message = _get_grammar()

    data = "hello\n    reee\n\tgoodbye"
    first = parsenow(message, data)
    asserttip(first['the_hello'], "hello", where=(1, 0))
    asserttip(first["the_reee"], "reee", where=(2, 4))
    asserttip(first['the_goodbye'], "goodbye", where=(3, 1))


def test_space_combinations():
    message = _get_grammar()

    data = "hello\n  \treee\t\n\t  \n\tgoodbye"
    first = parsenow(message, data)
    asserttip(first['the_hello'],   "hello",   where=(1, 0))
    asserttip(first["the_reee"],    "reee",    where=(2, 3))
    asserttip(first['the_goodbye'], "goodbye", where=(4, 1))
