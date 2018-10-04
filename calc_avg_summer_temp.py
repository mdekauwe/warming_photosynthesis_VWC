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


def main(flux_dir, met_dir, output_dir):

    pass


if __name__ == "__main__":


    flux_dir = "data/Flux/"
    met_dir = "data/Met/"
    output_dir = "outputs"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    main(flux_dir, met_dir, output_dir)
