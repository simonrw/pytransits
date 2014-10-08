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

