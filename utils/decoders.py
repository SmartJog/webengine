# Decoders


class Decoder:
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
        super().__init__()
        self._input = "xml"

    def decode(self, obj):
        super().decode(obj)
        # TODO


class SoapDecoder(Decoder):
    def __init__(self):
        super().__init__()
        self._input = "soap"

    def decode(self, obj):
        super().decode(obj)
        # TODO


class JSONDecoder(Decoder):
    def __init__(self):
        super().__init__()
        self._input = "json"

    def decode(self, obj):
        super().decode(obj)
        import json

        return json.JSONDecoder().decode(obj.decode())


class DefaultDecoder(Decoder):
    def __init__(self):
        super().__init__()
        self._input = "default"

    def decode(self, obj):
        super().decode(obj)
        return str(obj)


class PickleDecoder(Decoder):
    def __init__(self):
        super().__init__()
        self._input = "pickle"

    def decode(self, obj):
        super().decode(obj)
        import pickle

        return pickle.loads(obj)


class MsgpackDecoder(Decoder):
    def __init__(self):
        super().__init__()
        self._input = "msgpack"

    def decode(self, obj):
        super().decode(obj)
        import msgpack

        return msgpack.unpackb(obj, raw=False, strict_map_key=False)


class DecoderFactory:
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
