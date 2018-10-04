#!/usr/bin/env python

"""
For each FLUX site, calculate the mean summer temperature for each site year.

That's all folks.
"""
__author__ = "Martin De Kauwe"
__version__ = "1.0 (04.10.2018)"
__email__ = "mdekauwe@gmail.com"


import os
import sys
import glob
import numpy as np
import xarray as xr
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd


def main(flux_files, met_files, output_dir):

    for i in flux_files:
        print(os.path.basename(i))


if __name__ == "__main__":

    flux_dir = "/Users/%s/research/all_fluxnet_files/flux" % (os.getlogin())
    met_dir = "/Users/%s/research/all_fluxnet_files/met" % (os.getlogin())
    output_dir = "outputs"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    flux_files = glob.glob(os.path.join(flux_dir, "*.nc"))
    met_files = glob.glob(os.path.join(met_dir, "*.nc"))

    main(flux_files, met_files, output_dir)
