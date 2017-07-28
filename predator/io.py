from predator.common import LINEBREAK_RE


class InputStream:
    """
    InputStream is an abstraction layer around a stream of text which allows
    inspecting the contents of the text in structured ways.
    """
    def __init__(self, data):
        self._lines = LINEBREAK_RE.split(data)

    @classmethod
    def fromfile(class_, path):
        # FIXME: this is not memory efficient
        with open(path, 'rU') as f:
            return class_(f.read())
