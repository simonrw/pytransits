#!/usr/bin/env python
# encoding: utf-8

from Modelgen import PyModel, PyGenerateSynthetic
import numpy as np
from numpy.random import normal, random
import matplotlib.pyplot as plt
import pyfits
from srw import exodb


def fit_goodness(flux, fluxerr, model_flux):
    '''
    Returns the goodness of fit for a certain data set with model
    '''

    assert flux.size == fluxerr.size == model_flux.size

    meanflux = np.average(flux, weights=1. / fluxerr ** 2)
    normflux = flux / meanflux

    # Do the chi square test
    return np.sum(((normflux - model_flux) / fluxerr) ** 2)


def get_data(filename):
    # Open the wasp data file and get the lightcurve
    with pyfits.open(filename) as f:
        photometry = f[1].data

    return {
            'jd': photometry.field('tmid'),
            'flux': photometry.field('tamflux2'),
            'fluxerr': photometry.field('tamflux2_err'),
            }


def get_catalogue_data(planet_name):
    results = exodb.queryForColumns([
        'planet.name', 'system.period', 'system.epoch',
        'system.a', 'system.i', 'star.radius', 'planet.radius',
        'star.mass', 'star.teff'],
        where='replace(planet.name, " ", "") = "%s"' %
            planet_name.replace(" ", ""))

    if len(results):
        results = results[0]

        m = PyModel()
        m.period = float(results[1])
        m.epoch = float(results[2])
        m.a = float(results[3])
        m.i = float(results[4])
        m.rs = float(results[5])
        m.rp = float(results[6])
        m.mstar = float(results[7])
        m.teff = float(results[8])

        return m
    else:
        raise RuntimeError("Cannot create planet model")


if __name__ == '__main__':
    nIter = 1000

    init = get_catalogue_data("WASP-12 b")
    data = get_data('data/wasp12.fits')

    jd = np.array(data['jd'], dtype=np.float64)
    flux = data['flux']
    fluxerr = data['fluxerr']

    weights = 1. / fluxerr ** 2
    meanflux = np.average(flux, weights=weights)

    phase = (np.abs(jd - init.epoch) / init.period) % 1
    phase[phase > 0.8] -= 1.0

    flux /= meanflux

    model = PyGenerateSynthetic(jd, init)

    # Get the initial prob
    P = fit_goodness(flux, fluxerr, model)

    print "Initial P: %f" % P
    i = 0
    for i in xrange(nIter):
        new_model = PyModel()
        new_model.period = normal(init.period, 0.5)
        new_model.epoch = normal(init.epoch, 1.0)
        new_model.a = normal(init.a, 0.01)
        new_model.rs = normal(init.rs, 0.1)
        new_model.i = normal(init.period, 0.3)
        new_model.rp = normal(init.rp, 0.1)
        new_model.mstar = normal(init.mstar, 0.1)
        new_model.teff = normal(init.teff, 100.)

        new_P = fit_goodness(flux, fluxerr,
                PyGenerateSynthetic(jd, new_model)
                )

        a_ratio = new_P / P
        if a_ratio < 1. or random() <= a_ratio:
            # Accept the change
            P = new_P
            init = new_model

        if i % 10 == 0:
            print "Iteration %d" % i

    print "Final P: %f" % P

    model = PyGenerateSynthetic(jd, init)
    plt.plot(phase, flux, 'r.')
    plt.plot(phase, model, 'g.')
    plt.show()
