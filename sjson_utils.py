class CMD:
    values = ("ERROR", "ACK", "WORKER", "END")

    def __init__(self, value):
        self.data = "ERROR"
        if value in CMD.values:
            self.data = value

    def __repr__(self):
        return "<CMD: %s>" % self.data


def json_object_hook(dct):
    if '__complex__' in dct:
        return complex(dct['real'], dct['imag'])
    if '__CMD__' in dct:
        return CMD(CMD.values[dct['__CMD__']])
    if '__classobj__' in dct:
        mod = __import__(dct['module'])
        return getattr(mod, dct['name'])
    return dct


def json_default(obj):
    if isinstance(obj, complex):
        return {"__complex__": True, "real": obj.real, "imag": obj.imag}
    elif isinstance(obj, CMD):
        return {"__CMD__": CMD.values.index(obj.data)}
    elif type(obj).__name__ == "classobj":
        return {
            "__classobj__": True,
            "module": obj.__module__,
            "name": obj.__name__
        }
