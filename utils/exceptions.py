# Exceptions for webengine

class ImpossibleRenderingException(Exception):
    """ Raise when it seems to be impossible to render this view. """
    def __init__(self, str):
        self.str = str
    def __str__(self):
        return str(self.str)
