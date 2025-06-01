import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

df_input = pd.read_excel('data/idoc-knobloch.xlsx',
                         usecols=['sediment_depth_m', 'absolute_elevation_dhhn', 'depth_sat_zone', 'rel_elevation_point1', 'idoc_mgl', 'meas_station', 'site_name'],
                         )

# Create array for subsequent loop
meas_array = df_input['site_name'].unique().tolist()

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
    fig, ax = plt.subplots(figsize=(3.5/1.3, 3.5/1.3))
    meas_array_site = df_input[df_input['site_name'] == site]
    meas_array_site_list = meas_array_site['meas_station'].unique().tolist()
    print(meas_array_site_list)
    # Loop through values computed with different q approaches
    for meas in meas_array_site_list:
        df_toplot = df_input[df_input['meas_station'] == meas]
        rel_location  = str(df_toplot['meas_station'].iloc[0])
        _, rel_location_plt = rel_location.split('-')
        df_toplot.plot(x='idoc_mgl',
                       y='depth_sat_zone',
                       color=nested_colors[rel_location_plt],
                       ax=ax,
                       label=meas,
                       grid=True,
                       marker=nested_markers[rel_location_plt],
                       markerfacecolor=nested_colors[rel_location_plt],
                       markeredgewidth=0.3,  # Set the edge thickness
                       markeredgecolor='black')
    ax.fill_between(x=[0, 12], y1=0, y2=-1, color='#1f77b4', alpha=0.3)
    ax.set_xlabel('DO [mg/L]')
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

    ax.set_xlim(0, 12)
    x_tick_interval = 3  # Adjusted to give similar visual spacing to y-axis
    ax.set_xticks(np.arange(0, 13, x_tick_interval))

    # Calculate the aspect ratio based on the limits to ensure approximately equal spacing between ticks
    x_range = ax.get_xlim()[1] - ax.get_xlim()[0]
    y_range = ax.get_ylim()[0] - ax.get_ylim()[1]
    ax.set_aspect(abs(x_range / y_range))  # Set aspect ratio close to 1

    ax.get_legend().remove()
    plt.tight_layout()
    fig.savefig('ido-' + str(site) + '.png', dpi=300)
