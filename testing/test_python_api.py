from transitgen import Model
import pytest

model_params = ['period', 'epoch', 'a', 'rs', 'i', 'rp', 'mstar',
                'c1', 'c2', 'c3', 'c4', 'teff']

def test_model_constructor():
    m = Model()

    for param in model_params:
        assert getattr(m, param) == 0

def test_class_constructor():
    m = Model.from_params({
        key: value for (value, key) in enumerate(model_params)
    })

    for i, param in enumerate(model_params):
        assert getattr(m, param) == i


def test_set_ldc():
    m = Model()
    m.set_ldc([1, 2, 3, 4])

    assert m.c1 == 1
    assert m.c2 == 2
    assert m.c3 == 3
    assert m.c4 == 4

def test_types_match():
    from transitgen._Modelgen import _check_types
    from numpy import arange
    assert _check_types(arange(10), Model())
