from transitgen import Model

model_params = ['period', 'epoch', 'a', 'rs', 'i', 'rp', 'mstar',
                'c1', 'c2', 'c3', 'c4', 'teff']

def test_model_constructor():
    m = Model()

    for param in model_params:
        assert getattr(m, param) == 0
