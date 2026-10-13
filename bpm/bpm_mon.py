#!/usr/bin/python3

"""
MOLLER TARGET BPM MONITOR

Based on Hall C target_bpm.py
Currently using the Hall C BPMs for testing

Reads BPM positions from EPICS, applies the slope/offset calibration and
projects the beam to the target with a straight-line fit through the
selected BPMs.

Adding a BPM:   add one BPM(...) line to BPM_TABLE below.
Fit selection:  set use_fit in BPM_TABLE (default at startup), or toggle
                the check boxes in the GUI while it is running.

Examples:
  ./bpm_mon.py                          # normal running
  ./bpm_mon.py --sim                    # random values, no EPICS needed
"""

import sys
import time
import random
import argparse
import textwrap
from dataclasses import dataclass
from typing import Optional

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
from scipy.odr import Model, RealData, ODR

#-----------------------------------------------------
# Configuration, calibration parameters
# Change as needed
#-----------------------------------------------------

# BCM
BCM_NAME = "IBC3H00CRCUR4"
BCM_CUT = 0.1

# Target
ZTAR = 0.0                       # cm, target z position
TARGET_NOMINAL = (-0.06, 0.29)   # mm, nominal (x, y) on target

UPDATE_PERIOD = 1.5              # s, between EPICS reads
POS_TEXT_SIZE = 18               # font size of the target position readout


@dataclass
class BPM:
    """ One beam position monitor.

    name          : EPICS name without the 'IPM' prefix (PVs are IPM<name>.XPOS/.YPOS)
    z             : position along beamline, cm from target (upstream is negative)
    xslope/yslope : calibration slopes
    xoff/yoff     : offsets (mm), from harp scan
    dx/dy         : additional incremental corrections (mm), not from full calibration
    ex/ey         : position uncertainty used in the fit (mm)
    xnom/ynom     : nominal position (mm) for reference markers, None = no marker
    use_fit       : include in the target projection by default
    """
    name: str
    z: float
    xslope: float = 1.0
    yslope: float = 1.0
    xoff: float = 0.0
    yoff: float = 0.0
    dx: float = 0.0
    dy: float = 0.0
    ex: float = 0.1
    ey: float = 0.1
    xnom: Optional[float] = None
    ynom: Optional[float] = None
    use_fit: bool = True

    @property
    def pv(self):
        return "IPM" + self.name


# BPM table: add new BPMs here (order does not matter)
BPM_TABLE = [
    BPM('3H07A', z=-320.42,  xslope=1.02, yslope=0.99, xoff=-0.195, yoff= 0.131,
        xnom= 0.25, ynom=0.80),
    BPM('3H07B', z=-224.97,  xslope=1.06, yslope=1.18, xoff= 0.708, yoff=-0.091,
        xnom=-0.47, ynom=0.82),
    BPM('3H07C', z=-129.314, xslope=0.86, yslope=0.88, xoff= 0.549, yoff= 0.089,
        xnom=-0.70, ynom=0.80),
    # Example of an extra BPM, not used in the fit by default:
    # BPM('3H04', z=-450.0, xslope=1.0, yslope=1.0, use_fit=False),
]

#-----------------------------------------------------
# EPICS access
#-----------------------------------------------------

caget = None   # set in init_epics()


def _sim_caget(pv, **kwargs):
    """ Stand-in for epics.caget, for testing without EPICS """
    if pv == BCM_NAME:
        return 5.0
    return random.gauss(0.0, 0.3)


def init_epics(sim=False):
    global caget
    if sim:
        caget = _sim_caget
    else:
        from epics import caget as epics_caget
        caget = epics_caget


ERROR_REPEAT = 600   # s, how often to repeat a message for a PV that stays bad
_pv_errors = {}      # pv -> time of last message, only while the PV is failing


def _report(pv, msg):
    """ Print a PV problem once, then at most every ERROR_REPEAT seconds,
    so a PV that is down for days does not flood the console/log """
    now = time.time()
    last = _pv_errors.get(pv)
    if last is None or now - last >= ERROR_REPEAT:
        stamp = time.strftime('%Y-%m-%d %H:%M:%S')
        repeat = "" if last is None else " (still failing)"
        print(f"{stamp} {msg}{repeat}", flush=True)
        _pv_errors[pv] = now


def safe_caget(pv):
    """ caget that returns None (with a rate-limited message) instead of raising """
    try:
        val = caget(pv)
    except Exception as ex:
        _report(pv, f"EPICS caget failed for {pv}: {ex}")
        return None
    if val is None:
        _report(pv, f"EPICS PV {pv} returned None")
        return None
    if pv in _pv_errors:
        del _pv_errors[pv]
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} EPICS PV {pv} OK again", flush=True)
    return val


def get_bcm():
    """ Beam current, 0.0 if it cannot be read """
    val = safe_caget(BCM_NAME)
    return 0.0 if val is None else val


def read_bpms(bpms):
    """ Raw X/Y readings (mm). A BPM that cannot be read gives NaN,
    so it is left out of the fit instead of being treated as 0.0 """
    xraw = np.full(len(bpms), np.nan)
    yraw = np.full(len(bpms), np.nan)
    for i, b in enumerate(bpms):
        x = safe_caget(b.pv + ".XPOS")
        y = safe_caget(b.pv + ".YPOS")
        if x is not None:
            xraw[i] = x
        if y is not None:
            yraw[i] = y
    return xraw, yraw

#-----------------------------------------------------
# Calibration and fit
#-----------------------------------------------------

class Calibration:
    """ Per-BPM calibration constants as vectors, in BPM list order """
    def __init__(self, bpms):
        def col(attr):
            return np.array([getattr(b, attr) for b in bpms], dtype=float)
        self.z = col('z')
        self.xslope, self.yslope = col('xslope'), col('yslope')
        self.xoff = col('xoff') + col('dx')
        self.yoff = col('yoff') + col('dy')
        self.ex, self.ey = col('ex'), col('ey')

    def apply(self, xraw, yraw):
        return xraw * self.xslope + self.xoff, yraw * self.yslope + self.yoff


def f(B, x):
    """ Linear function y = m*x + b, for ODR fitting.
    B = [slope, intercept] """
    return B[0]*x + B[1]


def fit_line(z, pos, err):
    """ Straight-line fit, returns [slope, intercept] or None.
    NaN points are skipped. Needs at least 2 points; with exactly 2
    the line goes through both. """
    ok = np.isfinite(pos)
    z, pos, err = z[ok], pos[ok], err[ok]
    if len(z) < 2:
        return None
    beta0 = np.polyfit(z, pos, 1, w=1.0/err)
    if len(z) == 2:
        return beta0
    out = ODR(RealData(z, pos, sy=err), Model(f), beta0=beta0).run()
    return out.beta

#-----------------------
# Plots
#-----------------------

def update_errorbar(container, x, y, err):
    """ Update an ErrorbarContainer in place (number of points may change) """
    plotline, caplines, barlinecols = container.lines
    x, y, err = np.asarray(x), np.asarray(y), np.asarray(err)
    plotline.set_data(x, y)
    if barlinecols:
        segs = [np.array([[xi, yi - ei], [xi, yi + ei]])
                for xi, yi, ei in zip(x, y, err)]
        barlinecols[0].set_segments(segs)


def setup_plot(bpms, cal):
    """ Create the figure and all artists, done once """
    plt.ion()
    fig = plt.figure(figsize=(12, 7))
    fig.subplots_adjust(left=0.17, right=0.92, top=0.88, wspace=0.08)

    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(223, sharex=ax1)
    ax3 = fig.add_subplot(122)

    z = cal.z
    zlo = min(z.min(), ZTAR) - 50
    zhi = max(z.max(), ZTAR) + 50
    zfit = np.linspace(zlo, zhi, 500)
    empty = np.array([])

    plot = {'fig': fig, 'ax1': ax1, 'ax2': ax2, 'ax3': ax3, 'zfit': zfit}

    for ax, axis, err in ((ax1, 'x', cal.ex), (ax2, 'y', cal.ey)):
        nom = [(b.z, getattr(b, axis + 'nom')) for b in bpms
               if getattr(b, axis + 'nom') is not None]
        if nom:
            zn, pn = zip(*nom)
            ax.plot(zn, pn, marker='s', color='b', markersize=8,
                    fillstyle='none', linestyle='none')
        nan = np.full(len(bpms), np.nan)
        plot[axis + '_raw'] = ax.errorbar(z, nan, yerr=err, fmt='o',
                                          color='b', markersize=4)
        plot[axis + '_fit_pts'] = ax.errorbar(empty, empty, yerr=empty, fmt='o',
                                              color='r', markersize=4)
        plot[axis + '_nofit_pts'] = ax.errorbar(empty, empty, yerr=empty, fmt='o',
                                                color='0.6', markersize=4)
        plot[axis + '_fit'], = ax.plot(zfit, np.full_like(zfit, np.nan), color='r')
        ax.axvline(ZTAR, color='k', linestyle=':', linewidth=1)
        ax.set_xlim(zlo, zhi)
        ax.set_ylim(-2, 2)
        ax.set_ylabel(f'{axis.upper()} (mm)', fontsize=15)

    # BPM names along the top of the X plot
    for b in bpms:
        ax1.text(b.z, 1.02, b.name, transform=ax1.get_xaxis_transform(),
                 ha='center', va='bottom', fontsize=8)
    plt.setp(ax1.get_xticklabels(), visible=False)
    ax2.set_xlabel('Z, Distance from target (cm)', fontsize=15)

    # Projection to target
    nom_pt, = ax3.plot([TARGET_NOMINAL[0]], [TARGET_NOMINAL[1]], marker='s',
                       color='b', markersize=8, fillstyle='none', linestyle='none')
    plot['tar_pos'], = ax3.plot([np.nan], [np.nan], marker='o', color='r',
                                markersize=4, linestyle='none')
    ax3.yaxis.tick_right()
    ax3.yaxis.set_label_position('right')
    ax3.grid(color='grey')
    ax3.set_xlabel('Target X (mm)', fontsize=15)
    ax3.set_ylabel('Target Y (mm)', fontsize=15)
    ax3.set_xlim(-4, 4)
    ax3.set_ylim(-2, 2)
    plot['pos_text'] = ax3.text(0.5, 0.96, "", transform=ax3.transAxes,
                                ha='center', va='top', multialignment='center',
                                fontsize=POS_TEXT_SIZE,
                                bbox=dict(facecolor='white', edgecolor='none', alpha=0.8))
    ax3.legend([plot['y_raw'], plot['y_fit_pts'], plot['y_nofit_pts'], nom_pt],
               ['Raw BPM position', 'True position (in fit)',
                'True position (not in fit)', 'Nominal position'],
               loc='lower left', fontsize=9)

    # Nominal positions of all BPMs, wrapped to the figure width
    noms = [f"{b.name}: ({b.xnom}, {b.ynom})" for b in bpms if b.xnom is not None]
    if noms:
        fig.text(0.17, 0.97, "\n".join(textwrap.wrap("Nominal " + ", ".join(noms), 140)),
                 va='top', fontsize=10)

    # Check boxes to choose the BPMs used in the projection
    names = [b.name for b in bpms]
    h = 0.035 * len(bpms) + 0.02
    rax = fig.add_axes([0.01, 0.5 - h/2, 0.10, h])
    rax.set_title('Use in fit', fontsize=10)
    plot['check'] = CheckButtons(rax, names, [b.use_fit for b in bpms])
    return plot


def refresh(plot, state, cal):
    """ Redo the fit from the latest readings and redraw """
    use = np.array(plot['check'].get_status(), dtype=bool)
    z = cal.z
    beam_on = state['bcm'] > BCM_CUT

    tar = {}
    for axis, err in (('x', cal.ex), ('y', cal.ey)):
        raw, cor = state[axis + 'raw'], state[axis + 'cor']
        update_errorbar(plot[axis + '_raw'], z, raw, err)
        update_errorbar(plot[axis + '_fit_pts'], z[use], cor[use], err[use])
        update_errorbar(plot[axis + '_nofit_pts'], z[~use], cor[~use], err[~use])

        beta = fit_line(z[use], cor[use], err[use]) if beam_on else None
        if beta is None:
            plot[axis + '_fit'].set_ydata(np.full_like(plot['zfit'], np.nan))
            tar[axis] = None
        else:
            plot[axis + '_fit'].set_ydata(f(beta, plot['zfit']))
            tar[axis] = f(beta, ZTAR)

    if not beam_on:
        msg = f"Beam current {state['bcm']:.2f} below cut ({BCM_CUT})"
    elif tar['x'] is None or tar['y'] is None:
        msg = "Need at least 2 working BPMs\nselected for the fit"
    else:
        msg = f"Beam position on target:\n{tar['x']:.2f} , {tar['y']:.2f}"

    if tar.get('x') is not None and tar.get('y') is not None:
        plot['tar_pos'].set_data([tar['x']], [tar['y']])
    else:
        plot['tar_pos'].set_data([np.nan], [np.nan])
    plot['pos_text'].set_text(msg)
    plot['fig'].canvas.draw_idle()

#-----------------------
# Main program
#-----------------------

def get_bpm_list():
    """ All BPMs in BPM_TABLE, ordered along the beamline """
    bpms = sorted(BPM_TABLE, key=lambda b: b.z)
    if sum(b.use_fit for b in bpms) < 2:
        print("Warning: fewer than 2 BPMs selected for the fit; "
              "select more in the GUI to get a projection")
    return bpms


def parse_args():
    p = argparse.ArgumentParser(description="MOLLER target BPM monitor")
    p.add_argument('--period', type=float, default=UPDATE_PERIOD,
                   help=f"update period in seconds (default {UPDATE_PERIOD})")
    p.add_argument('--sim', action='store_true',
                   help="use random values instead of EPICS")
    return p.parse_args()


def main():
    args = parse_args()
    init_epics(args.sim)

    bpms = get_bpm_list()
    cal = Calibration(bpms)
    plot = setup_plot(bpms, cal)

    nan = np.full(len(bpms), np.nan)
    state = {'bcm': 0.0, 'xraw': nan, 'yraw': nan, 'xcor': nan, 'ycor': nan}

    # redraw right away when a check box is toggled
    plot['check'].on_clicked(lambda label: refresh(plot, state, cal))

    closed = {'flag': False}
    def on_close(event):
        closed['flag'] = True
    plot['fig'].canvas.mpl_connect('close_event', on_close)

    try:
        while not closed['flag']:
            state['bcm'] = get_bcm()
            state['xraw'], state['yraw'] = read_bpms(bpms)
            if state['bcm'] > BCM_CUT:
                state['xcor'], state['ycor'] = cal.apply(state['xraw'], state['yraw'])
            else:
                state['xcor'], state['ycor'] = nan, nan

            refresh(plot, state, cal)
            plt.pause(args.period)

    except KeyboardInterrupt:
        print("\nProgram stopped by the user")
    finally:
        if closed['flag']:
            print("Figure canvas closed, terminating the program")
        plt.close(plot['fig'])


if __name__ == "__main__":
    main()
