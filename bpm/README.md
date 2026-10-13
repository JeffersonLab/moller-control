# BPM monitor

Online monitoring GUI for the beam position monitors. It reads BPM values from EPICS and projects the position to the target using a straight line fit.

## Requirements
* Python 3.7 or later
* numpy, scipy, matplotlib, epics packages
* X display

## How to run
```
./bpm_mon.py             # normal running
./bpm_mon.py --sim       # test mode using random values
./bpm_mon.py --period 3  # update every 3s (default: 1.5s)
```

<img width="1191" height="694" alt="bpm_mon" src="https://github.com/user-attachments/assets/fcabe5af-4e7e-4a64-bae8-1d9bdf48b30d" />

### Adding BPMs
Update BPM_TABLE (example with Hall C BPMs):
```python
BPM_TABLE = [
    BPM('3H07A', z=-320.42,  xslope=1.02, yslope=0.99, xoff=-0.195, yoff= 0.131,
        xnom= 0.25, ynom=0.80),
    BPM('3H07B', z=-224.97,  xslope=1.06, yslope=1.18, xoff= 0.708, yoff=-0.091,
        xnom=-0.47, ynom=0.82),
    BPM('3H07C', z=-129.314, xslope=0.86, yslope=0.88, xoff= 0.549, yoff= 0.089,
        xnom=-0.70, ynom=0.80),
]
```
| Field             | Description                                                     | Default |
|-------------------|-----------------------------------------------------------------|---------|
| `name`            | EPICS name without the `IPM` prefix                             | —       |
| `z`               | Position along the beamline, cm from target (upstream negative) | —       |
| `xslope`/`yslope` | Calibration slopes                                              | 1.0     |
| `xoff`/`yoff`     | Offsets from harp scan (mm)                                     | 0.0     |
| `dx`/`dy`         | Additional incremental corrections (mm)                         | 0.0     |
| `ex`/`ey`         | Position uncertainty used to weight the fit (mm)                | 0.1     |
| `xnom`/`ynom`     | Nominal position for the reference markers (mm); omit for none  | none    |
| `use_fit`         | Whether the BPM is used in the fit at startup                   | True    |

Parameters to update:
* Nominal positions for each BPM
* Calibration parameters: slope parameters (xslope, yslope), target-lock offset from Harp scan calibration (xoff, yoff)
* Position uncertainty (weight) used in the fit: ex, ey

True (corrected) positions are calculated by
```
x = x_raw * xslope + xoff + dx
```
### Selecting BPMs to make the projection
* Initial selection for which BPMs to use in the fit is done by setting use_fit to True in the BPM_TABLE
* The selection can also be updated online using the left check boxes on the GUI (at least two BPMs are needed)
