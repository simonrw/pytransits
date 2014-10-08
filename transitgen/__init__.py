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

    def set_ldc(self, ldc):
        attrs = ['c1', 'c2', 'c3', 'c4']
        for (attr, value) in zip(attrs, ldc):
            setattr(self, attr, value)

def generate_synthetic(jd, model):
    return _Modelgen.PyGenerateSynthetic(jd, model)
