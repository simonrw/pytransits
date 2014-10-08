import _Modelgen

__all__ = ['Model', ]

class Model(object):
    def __init__(self):
        self._model = _Modelgen.PyModel()

    def __getattr__(self, attr):
        return getattr(self._model, attr)
