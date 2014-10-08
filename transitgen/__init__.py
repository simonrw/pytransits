import _Modelgen

__all__ = ['Model', ]

class Model(object):
    def __init__(self):
        self._model = _Modelgen.PyModel()

    @classmethod
    def from_params(cls, params):
        m = cls()
        for key in params:
            print(key)
            setattr(m, key, params[key])
        return m

    def __getattr__(self, attr):
        return getattr(self._model, attr)
