import os
import math
import numpy as np
import flopy.modflow as fpm
import pandas as pd
import flopy.utils.binaryfile as bf
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, FormatStrFormatter, LogLocator
from matplotlib.ticker import FuncFormatter

# If MinorLocator import is not working, import it directly from matplotlib
from matplotlib import ticker

def scientific_formatter(x, pos):
    exponent = int(np.log10(x)) if x != 0 else 0
    return r'$10^{{{}}}$'.format(exponent)

df_input = pd.read_excel('data/kfs-final-reord.xlsx')

# Create array for subsequent loop
meas_array = df_input['sample'].unique().tolist()

nested_colors = {'1': 'black',
                  '2': 'dimgrey',
                  '3': 'darkgrey',
                  '4': 'gainsboro',
                  'SW': 'black'}

nested_markers = {'1': 'o',
                  '2': 'x',
                  '3': 'd',
                  '4': 's',
                  'SW': None}

# Loop through measurement locations
for site in df_input['site_name'].unique().tolist():
    fig, ax = plt.subplots(figsize=(3.76/1.3, 3.5/1.3))
    meas_array_site = df_input[df_input['site_name'] == site]
    meas_array_site_list = meas_array_site['sample'].unique().tolist()
    print(meas_array_site_list)
    # Loop through values computed with different q approaches
    for meas in meas_array_site_list:
        df_toplot = df_input[df_input['sample'] == meas]
        rel_location  = str(df_toplot['sample'].iloc[0])
        _, rel_location_plt = rel_location.split('-')
        df_toplot.plot(x='Wooster et al. (2008) [Estimated kf]',
                       y='depth_sat_zone',
                       color=nested_colors[rel_location_plt],
                       ax=ax,
                       label=meas,
                       grid=True,
                       marker=nested_markers[rel_location_plt],
                       markerfacecolor=nested_colors[rel_location_plt],
                       markeredgewidth=0.3,  # Set the edge thickness
                       markeredgecolor='black')
    ax.set_xlabel('kf [m/s]')
    ax.set_ylabel('Saturated depth [m]')
    ax.xaxis.set_label_position('top')
    ax.xaxis.tick_top()

    # Set y-ticks and x-ticks to have proportional spacing
    ax.set_ylim(bottom=0.65, top=-0.1)
    y_tick_interval = 0.15  # Adjusted to give similar visual spacing to x-axis
    ax.set_yticks(np.arange(0, 0.7, y_tick_interval))
    y_ticks = ax.get_yticks()
    y_ticks = y_ticks[y_ticks != -0.1]
    ax.set_yticks(y_ticks)

    ax.set_xscale('log')
    ax.xaxis.set_major_formatter(FuncFormatter(scientific_formatter))
    ax.set_xlim(0.00001, 0.10)
    ax.set_xticks([0.00001, 0.0001, 0.001, 0.010, 0.1])

    # Add minor ticks
    ax.xaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1, numticks=12))
    ax.xaxis.set_minor_formatter(FormatStrFormatter(''))  # Hide the labels for minor ticks

    # ax.get_legend().remove()
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    fig.savefig('kf-' + str(site) + '.png', dpi=300)
