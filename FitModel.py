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

