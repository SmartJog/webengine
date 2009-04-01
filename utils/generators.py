# Generator

class Generator(object):
    def __init__(self):
        self._obj = None
        self._output = 'None'

    def generate(self, obj):
        self._obj = obj

    def __str__(self):
        if self._obj: return self.generate(self._obj)
        return "<Generator %s>" % str(self._output)

class XmlGenerator(Generator):
    def __init__(self):
        super(XmlGenerator, self).__init__()
        self._output = 'xml'

    def generate(self, obj):
        super(XmlGenerator, self).generate(obj)
        #TODO

class SoapGenerator(Generator):
    def __init__(self):
        super(SoapGenerator, self).__init__()
        self._output = 'soap'

    def generate(self, obj):
        super(SoapGenerator, self).generate(obj)
        #TODO

class JSONGenerator(Generator):
    def __init__(self):
        super(JSONGenerator, self).__init__()
        self._output = 'json'

    def generate(self, obj):
        super(JSONGenerator, self).generate(obj)
        import django.utils.simplejson as json
        return json.JSONEncoder().encode(obj)

class DefaultGenerator(Generator):
    def __init__(self):
        super(DefaultGenerator, self).__init__()
        self._output = 'default'

    def generate(self, obj):
        super(DefaultGenerator, self).generate(obj)
        return str(obj)

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
