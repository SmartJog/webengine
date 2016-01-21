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
        import json
        from django.core.serializers.json import DateTimeAwareJSONEncoder
        return json.dumps(obj, cls=DateTimeAwareJSONEncoder)

class PickleGenerator(Generator):
    def __init__(self):
        super(PickleGenerator, self).__init__()
        self._output = 'pickle'

    def generate(self, obj):
        super(PickleGenerator, self).generate(obj)
        import cPickle
        try:
            return cPickle.dumps(obj)
        except cPickle.PickleError, _error:
            # cPickle failed, try pickle
            import pickle
            return pickle.dumps(obj)

class MsgpackGenerator(Generator):
    def __init__(self):
        super(MsgpackGenerator, self).__init__()
        self._output = 'msgpack'

    def generate(self, obj):
        super(MsgpackGenerator, self).generate(obj)
        import msgpack
        return msgpack.packb(obj)

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
        'xml'    : XmlGenerator,
        'soap'   : SoapGenerator,
        'json'   : JSONGenerator,
        'pickle' : PickleGenerator,
        'default': DefaultGenerator,
        'msgpack': MsgpackGenerator,
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
