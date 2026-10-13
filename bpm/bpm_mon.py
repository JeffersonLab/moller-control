#!/usr/bin/python3

"""
MOLLER TARGET BPM MONITOR

Based on Hall C target_bpm.py
Currently using the Hall C BPMs for testing
"""

import sys
import math
import time
import random

import numpy as np
import matplotlib.pyplot as plt
from scipy.odr import Model, RealData, ODR
from epics import caget

#-----------------------------------------------------
# Configuration, calibration parameters
# Change as needed
#-----------------------------------------------------

# BCM
BCM_NAME = "IBC3H00CRCUR4"
BCM_CUT = 0.1

# BPM names
BPMS = ['3H07A', '3H07B', '3H07C'] 

# Z positions (cm from target)
ZPOS = np.array([-320.42, -224.97, -129.314])
ZTAR = 0.0 # at target

# Nominal X/Y positions, used for plotting reference markers
NOMINAL_POS = {
    'BPM1' : {'NAME':BPMS[0], 'XPOS': 0.25, 'YPOS': 0.80, 'ZPOS': ZPOS[0]},
    'BPM2' : {'NAME':BPMS[1], 'XPOS': -0.47,'YPOS': 0.82, 'ZPOS': ZPOS[1]},
    'BPM3' : {'NAME':BPMS[2], 'XPOS': -0.7, 'YPOS': 0.8,  'ZPOS': ZPOS[2]},
    'Target': {'NAME':'Target', 'XPOS': -0.06, 'YPOS': 0.29, 'ZPOS':ZTAR},
}

# X, Y slope from calibration
XSLOPE = np.array([1.02, 1.06, 0.86])
YSLOPE = np.array([0.99, 1.18, 0.88])

#  from Harp scan, needed to set BPM XSOFs back to old values
XOFF = np.array([-0.195, 0.708, 0.549])
YOFF = np.array([ 0.131,-0.091, 0.089])

# Additional, incremental corrections, not fit from full calibration
DX = np.array([0.0, 0.0, 0.0])
DY = np.array([0.0, 0.0, 0.0])

# OFFSETS
XOFF = XOFF+DX
YOFF = YOFF+DY

EX = np.array([0.1, 0.1, 0.1])
EY = np.array([0.1, 0.1, 0.1])

#-----------------------------------------------------
# prepare 1D vector arrays 
#-----------------------------------------------------

XNOM = np.array([v['XPOS'] for k, v in NOMINAL_POS.items() if k != 'Target'])
YNOM = np.array([v['YPOS'] for k, v in NOMINAL_POS.items() if k != 'Target'])
ZVEC = np.array([v['ZPOS'] for k, v in NOMINAL_POS.items() if k != 'Target'])

XFIT = np.linspace(-400, 50, 1000)

#-----------------------------------------------------
# Support functions
#-----------------------------------------------------

# fit line using both x and y errors
def f(B, x):
    """ Linear function y = m*x + b, for ODR fitting

     B is a vector of the parameters; [slope, intercept]
     x is an array of the current x values.
     x is in the same format as the x passed to Data or RealData.

     Return an array in the same format as y passed to Data or RealData.
    """
    return B[0]*x + B[1]

def get_bcm():
    """ Read and return BCM value.
    Returns 0.0 (with a warning) if caget fails or returns None
    """
    try:
        val = caget(BCM_NAME)
    except Exception as ex:
        print(f"Failed to get BCM value ({BCM_NAME}): {ex}")
        return 0.0
    if val is None:
        print(f"BCM PV ({BCM_NAME}) returned None")
        return 0.0

    return val

def get_bpm():
    """ Get xpos, ypos values for the given list of BPMs
    Apply slope/offset calibration when beam current is above threshold
    Returns:
    XRAW, YRAW: raw BPM readings (mm)
    XVEC, YVEC: corrected positions (mm). Set to zero if BCM < threshold
    """

    bcm = get_bcm()

    XRAW, YRAW = [], []
    for name in BPMS:
        epics_name = "IPM" + name
        xval = 0.0
        yval = 0.0
        try:
            xval = caget(epics_name + ".XPOS")
            yval = caget(epics_name + ".YPOS")
            #xval = random.gauss(0, 1)
            #yval = random.gauss(0, 1)
        except Exception as ex:
            print(f"EPICS caget failed for {epics_name}: {ex}")

        XRAW.append(xval if xval is not None else 0.0)
        YRAW.append(yval if yval is not None else 0.0)

    if bcm > BCM_CUT:
        XVEC = np.array(XRAW) * XSLOPE + XOFF
        YVEC = np.array(YRAW) * YSLOPE + YOFF
    else:
        XVEC = np.array(XRAW) * 0.0
        YVEC = np.array(YRAW) * 0.0

    return np.array(XRAW), np.array(YRAW), XVEC, YVEC

def fit_target_pos(z, pos, err):
    linear = Model(f)
    mydata = RealData(z, pos, sy=err)
    myodr = ODR(mydata, linear, beta0=[1.0, 2.0])
    myoutput = myodr.run()
    return myoutput.beta, round(myoutput.beta[1], 2)

#-----------------------
# Plots, Main program
#-----------------------

def setup_plot():
    """
    Create the subplots and returns a dict of obj
    Done only once
    """

    plt.ion() # turn on interactive mode
    fig = plt.figure()
    
    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(223)
    ax3 = fig.add_subplot(122)
    
    zeros = np.zeros(len(BPMS))

    # X Position
    ax1.plot(ZVEC, XNOM, marker='s', color='b', markersize=8,
             fillstyle='none', linestyle='none')
    x_raw = ax1.errorbar(ZVEC, zeros, yerr=EX, fmt='o', color='b', markersize=4)
    x_cor = ax1.errorbar(ZVEC, zeros, yerr=EX, fmt='o', color='r', markersize=4)
    x_fit_line, = ax1.plot(XFIT, np.zeros_like(XFIT), color='b')    
    ax1.set_ylim([-2,2])
    ax1.set_ylabel('X (mm)', fontsize=15)
    ax2.set_xlabel('Z, Distance from target (cm)', fontsize=15)
    
    # Y Position
    ax2.plot(ZVEC, YNOM, marker='s', color='b', markersize=8,
             fillstyle='none', linestyle='none')
    y_raw = ax2.errorbar(ZVEC, zeros, yerr=EY, fmt='o', color='b', markersize=4)
    y_cor = ax2.errorbar(ZVEC, zeros, yerr=EY, fmt='o', color='r', markersize=4)
    y_fit_line, = ax2.plot(XFIT, np.zeros_like(XFIT), color='b')
    ax2.set_ylim([-2, 2])
    ax2.set_ylabel('Y (mm)', fontsize=15)
    ax2.set_xlabel('Z, Distance from target (cm)', fontsize=15)

    # Projection
    cPos, = ax3.plot(NOMINAL_POS['Target']['XPOS'], NOMINAL_POS['Target']['YPOS'],
                     marker='s', color='b', markersize=8, fillstyle='none', linestyle='none')
    tPos, = ax3.plot([0], [0], marker='o', color='r', markersize=4)

    ax3.yaxis.tick_right()
    ax3.yaxis.set_label_position('right')
    ax3.yaxis.grid(color='grey')
    ax3.xaxis.grid(color='grey')    
    ax3.set_xlabel('Target X (mm)', fontsize=15)
    ax3.set_ylabel('Target Y (mm)', fontsize=15)
    ax3.set_xlim([-4,4])
    ax3.set_ylim([-2,2])
    pos_text = ax3.text(-3, 1.2, "")
    
    ax3.legend([y_raw, y_cor, cPos],
               ['Raw BPM position', 'True position', 'Nominal position'],
               loc='lower left')

    ax3.text(-11.5, 2.5, "Nominal {}: ({}, {}), {}: ({}, {})".format(
        NOMINAL_POS['BPM1']['NAME'], NOMINAL_POS['BPM1']['XPOS'], NOMINAL_POS['BPM1']['YPOS'],
        NOMINAL_POS['BPM2']['NAME'], NOMINAL_POS['BPM2']['XPOS'], NOMINAL_POS['BPM2']['YPOS']),
        size=10)
    
    # return dict of fig, plot obj
    return { 'fig':fig, 'ax1':ax1, 'ax2':ax2, 'ax3':ax3,
             'x_raw':x_raw, 'x_cor':x_cor, 'x_fit':x_fit_line,
             'y_raw':y_raw, 'y_cor':y_cor, 'y_fit':y_fit_line,
             'tar_pos':tPos,'pos_text':pos_text,
            }

def update_plot(container, x, y, err):
    # Update errorbar plot
    # ErrorbarContainer obj has three separate sub-artists
    # that need to be updated individually
    
    plotline, caplines, barlinecols = container.lines
    x = np.asarray(x)
    y = np.asarray(y)
    plotline.set_data(x, y)
    if barlinecols:
        err = np.asarray(err)
        new_segments = [np.array([[xi, yi - ei], [xi, yi + ei]]) for xi, yi, ei in zip(x, y, err)]
        barlinecols[0].set_segments(new_segments)

def main():

    # initialize plot obj
    dict_plot = setup_plot()

    closed = {'flag': False}

    def on_close(event):
        closed['flag'] = True

    dict_plot['fig'].canvas.mpl_connect('close_event', on_close)

    try:
        while not closed['flag']:
            
            XRAW, YRAW, XVEC, YVEC = get_bpm()
            
            # Linear fit to get positions at target
            beta_x, xtar = fit_target_pos(ZVEC, XVEC, EX)
            beta_y, ytar = fit_target_pos(ZVEC, YVEC, EY)

            # Update xraw, xcor data
            update_plot(dict_plot['x_raw'], ZVEC, XRAW, EX)
            update_plot(dict_plot['x_cor'], ZVEC, XVEC, EX)
            dict_plot['x_fit'].set_ydata(f(beta_x, XFIT))

            # Update for yraw, ycor
            update_plot(dict_plot['y_raw'], ZVEC, YRAW, EY)
            update_plot(dict_plot['y_cor'], ZVEC, YVEC, EY)
            dict_plot['y_fit'].set_ydata(f(beta_y, XFIT))

            dict_plot['tar_pos'].set_data([xtar], [ytar])
            dict_plot['pos_text'].set_text("Beam position on target:\n" + 8 * " " + str(xtar) + " , " + str(ytar))
            
            dict_plot['fig'].canvas.draw()
            dict_plot['fig'].canvas.flush_events()

            plt.pause(1.5)
            #gc.collect() # python calls automatically 
            
    except KeyboardInterrupt:
        print("\nProgram stopped by the user")
    finally:
        if closed['flag']:
            print("Figure canvas closed, terminating the program")
        plt.close(dict_plot['fig'])

if __name__=="__main__":
    main()
