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


def main(fname):

    df = pd.read_csv(fname)
    sites = np.unique(df.site)
    idx = np.arange(len(sites))

    width = 14
    height = 5
    fig = plt.figure(figsize=(width, height))
    fig.subplots_adjust(hspace=0.05)
    fig.subplots_adjust(wspace=0.02)
    plt.rcParams['text.usetex'] = False
    plt.rcParams['font.family'] = "sans-serif"
    plt.rcParams['font.sans-serif'] = "Helvetica"
    plt.rcParams['axes.labelsize'] = 16
    plt.rcParams['font.size'] = 16
    plt.rcParams['legend.fontsize'] = 12
    plt.rcParams['xtick.labelsize'] = 16
    plt.rcParams['ytick.labelsize'] = 16

    ax = fig.add_subplot(111)
    cnt = 1
    site_names = []
    cnts = []
    for i,site in enumerate(sites):
        df_site = df[df.site == site]
        tair = df_site.tair.values

        if tair[-1] - tair[0] > 3.0:
            #ax.plot(cnt, tair[0]-tair[0], "bo")
            ax.plot(cnt, tair[-1]-tair[0], "ro")
            site_names.append(site)
            cnts.append(cnt)
            cnt += 1

    ax.set_xticks(cnts)
    ax.set_xticklabels(site_names, rotation=45)
    ax.set_ylabel("Delta Tair")
    ax.set_ylim(0, 8)

    fig.savefig("sites_with_big_temp_diffs.pdf",
                bbox_inches='tight', pad_inches=0.1)
if __name__ == "__main__":

    fname = "outputs/site_tair.csv"
    main(fname)
