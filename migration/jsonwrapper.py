#!/usr/bin/python

class JsonWrapper:
    """
    simple wrapper to select an available and hopefully optimal json module
    """

    def __init__(self):
        known_modules = (
            ("json", "dumps", "loads"),
            ("cjson", "encode", "decode"),
            ("simplejson", "dumps", "loads"),
            ("json", "write", "read"),
        )
        for conf in known_modules:
            try:
                module = __import__ (conf[0])
                self.dumps = getattr(module, conf[1])
                self.loads = getattr(module, conf[2])
                dummy = self.dumps({"test": "ok"})
                if self.loads(dummy)["test"] == "ok":
                    return
            except:
                pass

json = JsonWrapper()
