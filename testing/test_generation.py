from Modelgen import PyModel, PyGenerateSynthetic
import numpy as np
import pytest
import matplotlib.pyplot as plt

jd = np.linspace(0, 3.2, 1000)
jd += 2454508.2


def generate_model():
    m = PyModel()
    m.id = 0
    m.submodel_id = 0
    m.period = 1.09
    m.epoch = 2454508.9
    m.a = 0.022
    m.rs = 1.54
    m.i = 89.2
    m.rp = 1.769
    m.mstar = 1.09
    m.c1 = 0.2
    m.c2 = 0.5
    m.c3 = -0.1
    m.c4 = -0.01
    m.teff = 6400.
    return m


def test_generation():
    m = generate_model()

    flux = PyGenerateSynthetic(jd, m)
    assert len(flux)

    for f in flux:
        assert f


def test_plot_lightcurve():
    m = generate_model()

    flux = PyGenerateSynthetic(jd, m)

    plt.plot(jd, flux, 'ro')
    plt.savefig("lightcurve.pdf")


def test_bad_arguments():
    with pytest.raises(TypeError) as e:
        PyGenerateSynthetic(jd, [1, 2, 3])

    assert "PyModel" in str(e)

    with pytest.raises(TypeError) as e:
        PyGenerateSynthetic("hello", generate_model())

    assert "numpy array" in str(e)
