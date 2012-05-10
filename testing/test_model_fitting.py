from FitModel import fit_goodness, get_data, get_catalogue_data, alter
from _Modelgen import PyModel
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


def test_random_number_gen_nonnegative():
    orig = 1.

    nez = 0
    for i in xrange(10000):
        newval = alter(orig, 1000., alter=True)
        assert newval > 0
        if newval != 1.:
            nez += 1

    assert nez > 0


def test_random_non_alter():
    val = 10.

    neq = 0
    for i in xrange(10000):
        newval = alter(val, 1000., alter=False)

        if newval != val:
            neq += 1

    assert neq == 0



def test_random_number_gen_negative():
    orig = 1.
    lz = 0
    nez = 0
    for i in xrange(10000):
            newval = alter(orig, 1000., alter=True, negative=True)
            if newval <= 0:
                lz += 1

            if newval != 1.:
                nez += 1

    assert lz > 0
    assert nez > 0
