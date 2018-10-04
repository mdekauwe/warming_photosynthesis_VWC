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

    for flux_fname, met_fname in zip(flux_files, met_files):
        site = os.path.basename(flux_fname).split(".")[0][0:6]
        years = os.path.basename(flux_fname).split(".")[0][7:16]
        source = os.path.basename(flux_fname).split(".")[0][17:].\
                                                  split("_")[0]
        print(site, years, source)

        (df_flx, df_met) = get_data(flux_fname, met_fname)
        (df_flx, df_met) = screen_files(df_flx, df_met, source)

        sys.exit()

def get_data(flux_fname, met_fname):

    ds = xr.open_dataset(flux_fname)
    df_flx = ds.squeeze(dim=["x","y"], drop=True).to_dataframe()
    df_flx = df_flx.reset_index()
    df_flx = df_flx.set_index('time')

    ds = xr.open_dataset(met_fname)
    df_met = ds.squeeze(dim=["x","y"], drop=True).to_dataframe()
    df_met = df_met.reset_index()
    df_met = df_met.set_index('time')

    # only keep "daylight" hours
    df_flx = df_flx.between_time("06:00", "20:00")
    df_met = df_met.between_time("06:00", "20:00")

    return (df_flx, df_met)

def screen_files(df_flx, df_met, source):

    KG_TO_G = 1000.0
    MOL_TO_MMOL = 1000.0
    G_TO_MOL_H20 = 1.0 / 18.0
    HPA_TO_KPA = 0.1
    KPA_TO_PA = 1000.0
    SEC_TO_HR = 3600.0
    SEC_TO_HLFHR = 1800.0
    UMOL_TO_MOL = 0.000001
    MOL_C_TO_GRAMS_C = 12.

    # Screen for measured and good gap-filled data
    if source == "OzFlux":
        # Measured = 0 ; 10 = instrument calibration correction,  good data
        df_met.where(np.logical_or(df_flx.GPP_qc == 0, df_flx.GPP_qc == 10),
                     inplace=True)

        # Measured = 0 ; 10 = instrument calibration correction,  good data
        df_flx.where(np.logical_or(df_flx.GPP_qc == 0, df_flx.GPP_qc == 10),
                     inplace=True)

    elif source == "FLUXNET2015":
        # Measured = 0 ; good-quality gap-fill = 1
        # No QC for GPP, use NEE and RECO
        df_met.where(np.logical_or(df_flx.NEE_qc == 0, df_flx.NEE_qc == 1),
                     inplace=True)

        # No QC for GPP, use NEE and RECO
        df_flx.where(np.logical_or(df_flx.NEE_qc == 0, df_flx.NEE_qc == 1),
                     inplace=True)

    elif source == "LaThuile":
        # Measured = 0 ; good-quality gap-fill = 1
        df_met.where(np.logical_or(df_flx.GPP_qc == 0, df_flx.GPP_qc == 1),
                     inplace=True)

        # Measured and good-quality gap fill
        df_flx.where(np.logical_or(df_flx.GPP_qc == 0, df_flx.GPP_qc == 1),
                     inplace=True)

    # Mask by met data.
    # Measured = 0 ; good-quality gap-fill = 1
    df_flx.where(np.logical_or(df_met.Tair_qc == 0, df_met.Tair_qc == 1),
                 inplace=True)
    df_met.where(np.logical_or(df_met.Tair_qc == 0, df_met.Tair_qc == 1),
                 inplace=True)


    diff = df_met.index.minute[1] - df_met.index.minute[0]
    if diff == 0:
        # hour gap i.e. Tumba
        df_flx["GPP"] *= MOL_C_TO_GRAMS_C * UMOL_TO_MOL * SEC_TO_HR
    else:
        # 30 min gap
        df_flx["GPP"] *= MOL_C_TO_GRAMS_C * UMOL_TO_MOL * SEC_TO_HLFHR

    # Drop the stuff we don't need
    df_flx = df_flx[['GPP']]
    df_met = df_met[['Tair']]

    df_met = df_met.reset_index()
    df_met = df_met.set_index('time')
    df_flx = df_flx.reset_index()
    df_flx = df_flx.set_index('time')

    (months, missing_gpp) = get_three_most_productive_months(df_flx)

    # filter three most productive months
    df_flx = df_flx[(df_flx.index.month == months[0]) |
                    (df_flx.index.month == months[1]) |
                    (df_flx.index.month == months[2])]
    df_met = df_met[(df_met.index.month == months[0]) |
                    (df_met.index.month == months[1]) |
                    (df_met.index.month == months[2])]

    return df_flx, df_met

def get_three_most_productive_months(df):
    # filter three most productive months
    df_m = df.resample("M").mean()
    missing_gpp = False

    try:
        df_m = df_m.sort_values("GPP", ascending=False)[:3]
        months = df_m.index.month
    except KeyError:
        missing_gpp = True
        months = None

    return (months, missing_gpp)

if __name__ == "__main__":

    flux_dir = "/Users/%s/research/all_fluxnet_files/flux" % (os.getlogin())
    met_dir = "/Users/%s/research/all_fluxnet_files/met" % (os.getlogin())
    output_dir = "outputs"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    flux_files = glob.glob(os.path.join(flux_dir, "*.nc"))
    met_files = glob.glob(os.path.join(met_dir, "*.nc"))

    main(flux_files, met_files, output_dir)
