# Decoders


class Decoder(object):
    def __init__(self):
        self._obj = None
        self._input = "None"

    def decode(self, obj):
        self._obj = obj

    def __str__(self):
        if self._obj:
            return self.decode(self._obj)
        return "<Decoder %s>" % str(self._input)


class XmlDecoder(Decoder):
    def __init__(self):
        super(XmlDecoder, self).__init__()
        self._input = "xml"

    def decode(self, obj):
        super(XmlDecoder, self).decode(obj)
        # TODO


class SoapDecoder(Decoder):
    def __init__(self):
        super(SoapDecoder, self).__init__()
        self._input = "soap"

    def decode(self, obj):
        super(SoapDecoder, self).decode(obj)
        # TODO


class JSONDecoder(Decoder):
    def __init__(self):
        super(JSONDecoder, self).__init__()
        self._input = "json"

    def decode(self, obj):
        super(JSONDecoder, self).decode(obj)
        import django.utils.simplejson as json

        return json.JSONDecoder().decode(obj)


class DefaultDecoder(Decoder):
    def __init__(self):
        super(DefaultDecoder, self).__init__()
        self._input = "default"

    def decode(self, obj):
        super(DefaultDecoder, self).decode(obj)
        return str(obj)


class PickleDecoder(Decoder):
    def __init__(self):
        super(PickleDecoder, self).__init__()
        self._input = "pickle"

    def decode(self, obj):
        super(PickleDecoder, self).decode(obj)
        import cPickle

        return cPickle.loads(obj)


class MsgpackDecoder(Decoder):
    def __init__(self):
        super(MsgpackDecoder, self).__init__()
        self._input = "msgpack"

    def decode(self, obj):
        super(MsgpackDecoder, self).decode(obj)
        import msgpack

        return msgpack.unpackb(obj)


class DecoderFactory(object):
    """DecoderFactory handles Decoder instances for the right input mode."""

    _input = {
        "xml": XmlDecoder,
        "soap": SoapDecoder,
        "json": JSONDecoder,
        "default": DefaultDecoder,
        "pickle": PickleDecoder,
        "msgpack": MsgpackDecoder,
    }

    @staticmethod
    def get(in_decoder):
        """
        Returns a valid Decoder instance for the given input mode.
        If the input mode is invalid, returns a DefaultDecoder.
        """

        decoder = "default"
        if in_decoder in DecoderFactory._input:
            decoder = in_decoder
        return DecoderFactory._input[decoder]()
