import importlib


class LazyModule:
    def __init__(self, name):
        self._module = None
        self.name = name

    @property
    def module(self):
        if not self._module:
            self._module = importlib.import_module(self.name)
        return self._module

    def __getattr__(self, name):
        return getattr(self.module, name)


def __getattr__(name):
    return LazyModule(name)
