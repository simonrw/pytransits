from FitModel import fit_goodness, get_data, get_catalogue_data
from Modelgen import PyModel
import pytest
import numpy as np


def check_close(val1, val2, toler):
    return ((val1 - val2) / val2) < toler


def test_goodness_function():
    flux = np.array([1., 2., 3.])
    fluxerr = np.ones_like(flux) * 0.1
    model_flux = np.array([1., 1., 1.])

    assert check_close(fit_goodness(flux, fluxerr, model_flux),
            ((3. * 10) + (2 * 10.)) ** 2,
            0.05)


def test_get_data():
    data = get_data('data/wasp12.fits')

    jd = data['jd']
    flux = data['flux']
    fluxerr = data['fluxerr']

    assert (jd.size == flux.size == fluxerr.size) > 0


def test_data_from_catalogue():
    results = get_catalogue_data('WASP-12b')
    assert type(results) == PyModel
    assert check_close(results.period, 1.09, 0.1)


def test_bad_data_retrieval():
    with pytest.raises(RuntimeError) as e:
        get_catalogue_data('badplanetname')

    assert 'planet model' in str(e)
