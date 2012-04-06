#!/usr/bin/env python
# encoding: utf-8

from Modelgen import PyModel, PyGenerateSynthetic
import numpy as np
import pyfits


def fit_goodness(flux, fluxerr, model_flux):
    '''
    Returns the goodness of fit for a certain data set with model
    '''

    assert flux.size == fluxerr.size == model_flux.size

    # Do the chi square test
    return np.sum(((flux - model_flux) / fluxerr) ** 2)


def get_data(filename):
    # Open the wasp data file and get the lightcurve
    with pyfits.open(filename) as f:
        photometry = f[1].data

    return {
            'jd': photometry.field('tmid'),
            'flux': photometry.field('tamflux2'),
            'fluxerr': photometry.field('tamflux2_err'),
            }
