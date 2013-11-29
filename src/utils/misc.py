import numpy as np
from scipy.constants import c, k, h

def fold(time, period, origo=0.0, shift=0.0, normalize=True,  clip_range=None):
    """Folds the given data over a given period.

    Parameters
    ----------
    
      time        
      period      
      origo       
      shift       
      normalize   
      clip_range  

    Returns
    -------

      phase       
    """
    tf = ((time - origo)/period + shift) % 1.

    if not normalize:
        tf *= period
        
    if clip_range is not None:
        mask = np.logical_and(clip_range[0]<tf, tf<clip_range[1])
        tf = tf[mask], mask
    return tf


def planck(T, wl):
    """Radiance as a function or black-body temperature and wavelength.

    Parameters
    ----------

      T   : Temperature  [K]
      wl  : Wavelength   [m]

    Returns
    -------

      B   : Radiance
    """
    return 2*h*c**2/wl**5 / (np.exp(h*c/(wl*k*T))-1)


def contamination_bb(c1, T, wl1, wl2):
    """Contamination from a third object radiating as a black-body given a contamination estimate in a reference wavelength. 

    Parameters
    ----------

      c1   : Contamination in the reference wavelength [-]
      T    : Temperature                               [K]
      wl1  : Reference wavelength                      [m]
      wl2  : Target wavelength                         [m]

    Returns
    -------

      c2  : Contamination in the given wavelength      [-]
    """
    B1   = planck(T, wl1)
    B2   = planck(T, wl2)

    return  c1*(B2/B1)