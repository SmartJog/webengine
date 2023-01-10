# Generator


class Generator:
    def __init__(self):
        self._obj = None
        self._output = "None"

    def generate(self, obj):
        self._obj = obj

    def __str__(self):
        if self._obj:
            return self.generate(self._obj)
        return "<Generator %s>" % str(self._output)


class XmlGenerator(Generator):
    def __init__(self):
        super().__init__()
        self._output = "xml"

    def generate(self, obj):
        super().generate(obj)
        # TODO


class SoapGenerator(Generator):
    def __init__(self):
        super().__init__()
        self._output = "soap"

    def generate(self, obj):
        super().generate(obj)
        # TODO


class JSONGenerator(Generator):
    def __init__(self):
        super().__init__()
        self._output = "json"

    def generate(self, obj):
        super().generate(obj)
        import json
        from django.core.serializers.json import DjangoJSONEncoder

        return json.dumps(obj, cls=DjangoJSONEncoder)


class PickleGenerator(Generator):
    def __init__(self):
        super().__init__()
        self._output = "pickle"

    def generate(self, obj):
        super().generate(obj)
        import pickle

        try:
            return pickle.dumps(obj)
        except pickle.PickleError as _error:
            # cPickle failed, try pickle
            import pickle

            return pickle.dumps(obj)


class MsgpackGenerator(Generator):
    def __init__(self):
        super().__init__()
        self._output = "msgpack"

    def generate(self, obj):
        super().generate(obj)
        import msgpack

        return msgpack.packb(obj, default=str)


class DefaultGenerator(Generator):
    def __init__(self):
        super().__init__()
        self._output = "default"

    def generate(self, obj):
        super().generate(obj)
        return str(obj)


class GeneratorFactory:
    """GeneratorFactory handles Generator instances for the right output mode."""

    _output = {
        "xml": XmlGenerator,
        "soap": SoapGenerator,
        "json": JSONGenerator,
        "pickle": PickleGenerator,
        "default": DefaultGenerator,
        "msgpack": MsgpackGenerator,
    }

    @staticmethod
    def get(output):
        """
        Returns a valid Generator instance for the given output mode.
        If the output mode is invalid, returns a DefaultGenerator.
        """

        out = "default"
        if output in GeneratorFactory._output:
            out = output
        return GeneratorFactory._output[out]()
