# Generator

class Generator(object):
    def __init__(self):
        pass

    def generate(self, obj):
        self._obj = obj

class XmlGenerator(Generator):
    def __init__(self):
        super(XmlGenerator, self).__init__()

    def generate(self):
        super(XmlGenerator, self).generate(obj)

class SoapGenerator(Generator):
    def __init__(self):
        super(SoapGenerator, self).__init__()

    def generate(self, obj):
        super(SoapGenerator, self).generate(obj)
 
class JSONGenerator(Generator):
    def __init__(self):
        super(JSONGenerator, self).__init__()

    def generate(self, obj):
        super(JSONGenerator, self).generate(obj)

class DefaultGenerator(Generator):
    def __init__(self):
        super(DefaultGenerator, self).__init__()

    def generate(self, obj):
        super(DefaultGenerator, self).generate(obj)

class GeneratorFactory(object):
    """ GeneratorFactory handles Generator instances for the right output mode. """
    _output = {
        'xml': XmlGenerator,
        'soap': SoapGenerator,
        'json': JSONGenerator,
        'default': DefaultGenerator,
    }

    @staticmethod
    def get(output):
        """
            Returns a valid Generator instance for the given output mode.
            If the output mode is invalid, returns a DefaultGenerator.
        """

        out = 'default'
        if output in GeneratorFactory._output:
            out = output
        return GeneratorFactory._output[out]()
