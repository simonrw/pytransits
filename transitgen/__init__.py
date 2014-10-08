import _Modelgen

__all__ = ['Model', ]

class Model(_Modelgen.PyModel):
    @classmethod
    def from_params(cls, params):
        m = cls()
        for key in params:
            print(key)
            setattr(m, key, params[key])
        return m

    def __getattr__(self, attr):
        return getattr(self._model, attr)
