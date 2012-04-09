#!/usr/bin/env python
# encoding: utf-8

from Modelgen import PyModel, PyGenerateSynthetic
import numpy as np
from numpy.random import normal, random
import copy
import matplotlib.pyplot as plt
import os.path
import pyfits
from srw import exodb
from PyLDC.LDC import PyLDC


def wd2jd(wd):
    jd_ref = 2453005.5
    jd = (wd / 86400.) + jd_ref
    return jd


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

        ldc = PyLDC(
                os.path.join(
                    os.path.expanduser("~"),
                    "work",
                    "ReferenceDatabase",
                    "Reference.db"),
                6
                )

        coeffs = ldc.coefficients(m.teff)

        m.c1 = coeffs[0]
        m.c2 = coeffs[1]
        m.c3 = coeffs[2]
        m.c4 = coeffs[3]

        return m
    else:
        raise RuntimeError("Cannot create planet model")


def mad(data, centre):
    return np.median(np.abs(data - centre))

def bin(phase, flux, fluxerr, N):
    '''
    Bin up into N phase bins
    '''
    inc = 1. / float(N)
    ledges = np.linspace(-0.2, 0.8 - inc, N)
    redges = ledges + inc

    centres = []
    out = []
    errs = []

    for l, r in zip(ledges, redges):
        ind = (phase >= l) & (phase < r)

        av = np.average(flux[ind], weights=1. / fluxerr[ind] ** 2)
        centres.append(l + inc / 2.)
        out.append(av)
        errs.append(1.25 * mad(flux[ind], av) / np.sqrt(flux[ind].size))



    return np.array(centres), np.array(out), np.array(errs)


def print_model(model):
    print 'Period: %f' % model.period
    print 'Epoch: %f' % model.epoch
    print 'RS: %f' % model.rs
    print 'RP: %f' % model.rp
    print 'a: %f' % model.a
    print 'i: %f' % model.i
    print 'mstar: %f' % model.mstar
    print 'teff: %f' % model.teff


def alter(orig, sigma, alter=True, negative=False):
    if not alter:
        return orig
    else:
        backup = copy.deepcopy(orig)

        offset = normal(0., sigma)
        new = backup + offset

        if not negative:
            while new <= 0.:
                offset = normal(0., sigma)
                new = backup + offset

            return new
        else:
            return new


def write_model(f, model):
    f.write('%f %f %f %f %f %f %f %f\n' % (
        model.period, model.epoch, model.a, model.rs,
        model.i, model.rp, model.mstar, model.teff)
        )



def copy_model(other):
    m = PyModel()

    m.period = other.period
    m.epoch = other.epoch
    m.a = other.a
    m.rs = other.rs
    m.i = other.i
    m.rp = other.rp
    m.mstar = other.mstar
    m.teff = other.teff
    m.c1 = other.c1
    m.c2 = other.c2
    m.c3 = other.c3
    m.c4 = other.c4

    return m


def add_model_to_hist(model, data):
    data['period'].append(model.period)
    data['epoch'].append(model.epoch)
    data['a'].append(model.a)
    data['rs'].append(model.rs)
    data['i'].append(model.i)
    data['rp'].append(model.rp)
    data['mstar'].append(model.mstar)
    data['teff'].append(model.teff)


if __name__ == '__main__':
    nIter = 1500

    init = get_catalogue_data("WASP-12 b")

    data = get_data('data/wasp12.fits')

    jd = np.array(wd2jd(data['jd']), dtype=np.float64)
    flux = data['flux']
    fluxerr = data['fluxerr']

    weights = 1. / fluxerr ** 2
    meanflux = np.average(flux, weights=weights)

    phase = (np.abs(jd - init.epoch) / init.period) % 1
    phase[phase > 0.8] -= 1.0

    flux /= meanflux
    fluxerr /= meanflux

    binned_phase, binned, binned_errs = bin(phase, flux, fluxerr, N=100)

    model = PyGenerateSynthetic(jd, init)

    logfile = open('log.txt', 'w')
    logfile.write('#period epoch a rs i rp mstar teff\n')

    #plt.plot(phase, flux, 'k.')
    #plt.errorbar(binned_phase, binned, binned_errs, ls="None")
    #plt.plot(binned_phase, binned, 'r.')
    #plt.plot(phase, model, 'g,')
    #plt.show()

    #exit()

    # Get the initial prob
    P = fit_goodness(flux, fluxerr, model)
    orig = copy.deepcopy(P)

    burn = 500
    thin = 1

    print "Before:"
    print_model(init)

    sigma = 0.001
    k = 0.999

    hist = {
            'period': [],
            'epoch': [],
            'a': [],
            'rs': [],
            'i': [],
            'rp': [],
            'mstar': [],
            'teff': [],
            }

    print "Initial P: %f" % P
    i = 0
    accepted = 0.
    rejected = 0.

    target_fraction = 0.23

    for i in xrange(nIter):
        new_model = copy_model(init)
        new_model.period = alter(new_model.period, sigma, False)
        new_model.epoch = alter(new_model.epoch, sigma, False)
        new_model.a = alter(new_model.a, sigma)
        new_model.rs = alter(new_model.rs, sigma)
        new_model.i = alter(new_model.i, sigma)
        new_model.rp = alter(new_model.rp, sigma)
        new_model.mstar = alter(new_model.mstar, sigma, False)
        new_model.teff = alter(new_model.teff, sigma, False)

        if i > burn and i % thin == 0:
            write_model(logfile, new_model)
            add_model_to_hist(new_model, hist)


        new_P = fit_goodness(flux, fluxerr,
                PyGenerateSynthetic(jd, new_model)
                )

        a_ratio = new_P / P

        if a_ratio < 1. or random() < a_ratio:
            # Accept the change
            #print '%d: New value accepted -> P: %f' % (i, new_P)
            P = copy.deepcopy(new_P)
            init = copy_model(new_model)

            accepted += 1.0
        else:
            rejected += 1.0

        try:
            fraction = accepted / rejected
        except ZeroDivisionError:
            fraction = 0.5

        if fraction < target_fraction:
            sigma /= k
        elif fraction > target_fraction:
            sigma *= k

        if i % 10 == 0:
            print "Iteration %d, fraction: %f, %f %f" % (i, fraction,
                    accepted, rejected)

    # Create the average model
    av_model = copy_model(init)
    av_model.period = np.average(hist['period'])
    av_model.epoch = np.average(hist['epoch'])
    av_model.rs = np.average(hist['rs'])
    av_model.a = np.average(hist['a'])
    av_model.rp = np.average(hist['rp'])
    av_model.mstar = np.average(hist['mstar'])
    av_model.teff = np.average(hist['teff'])
    av_model.i = np.average(hist['i'])

    print "Initial P: %f" % orig
    print "Final P: %f" % P

    logfile.close()

    print_model(av_model)

    model = PyGenerateSynthetic(jd, av_model)
    #plt.plot(phase, flux, 'r.')
    plt.errorbar(binned_phase, binned, binned_errs, ls='None')
    plt.plot(binned_phase, binned, 'r.')
    plt.plot(phase, model, 'g.')
    plt.show()

