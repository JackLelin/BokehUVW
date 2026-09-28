from bokeh.io import curdoc
from bokeh.layouts import column, row, gridplot, Spacer
from bokeh.models import ColumnDataSource, Select, Div, CheckboxButtonGroup, RadioButtonGroup, CustomJS, Slider, Range1d
import copy
from bokeh.models.widgets import Tabs, Panel, Dropdown
from bokeh.plotting import figure, output_file, show
from numpy.random import random, normal, lognormal
from numpy import roll,array
import numpy as np
from bokeh.models import Button
from glob import glob1
from bokeh.models.widgets import Dropdown
#from spc import spcs, year_images
import matplotlib.cm as cm
import matplotlib as mpl
from glob import glob1
global h_min, h_max, t_min, t_max, h_diff, t_diff, offset, entry_layout, years, color_menu, dname, year, sps, textboxes

#initializing a dummy variable date just for the webpage to run, this is changed when the user selects a year and date
dname = "/rd2/MST_ISR_EEJ_cont/processed/mesosphere/fit_gg/spc1min"
year = "2017"
date = "2017.04.20" 
yyyy = "2017"
mm = "04"
dd = "20"

years = sorted(glob1(dname, "*"))
year_menu = [(year, year) for year in years]
year_dropdown = Dropdown(label="Select a Year to explore.", button_type="success", menu=year_menu)

#datapath load
dpath_snr = dname + "/" + year + "/Maps/fitmap_" + date + ".npz" 
g = np.load(dpath_snr)
acqUTCtime = g['acqUTCtime']
"""Change UTC to local time (Peru)."""
localTime = acqUTCtime - 5*3600
"""Constrain time to 24 hours."""
localTime = localTime % (24*3600)

t_min = float(min(localTime)/3600)
t_max = float(max(localTime)/3600)
t_diff = t_max - t_min 

hts = g['hts']
h_min = min(hts) - .075
h_max = max(hts) - .3 + .75
h_diff = h_max - h_min 

colors = ['RdBu', 'plasma', 'viridis', 'gray', 'jet', 'RdBu_r']

Title_txt = Div(text = 'Mesospheric Winds at JRO', style={'font-size': '200%', 'color': 'black'}, width =1200)
Info_txt = Div(text = "This page contains a summary of the winds data measured at JRO during MST-ISR campaigns. To explore the data in an interactive mode click on the winds of the day of interest. By default the results shown are from the last analyzed year. Previous years can be selected using the drop-down list.")
 
#Colorbars
UVW_color_menu = Select(options = colors, value = colors[0], title = 'Color', width = 500)
RTI_color_menu = Select(options = colors, value = colors[-2], title = 'Color', width = 500)

#slider range endpoints
u_low = -80
u_high = 80
v_low = -100
v_high = 80
w_low = -3
w_high = 3
rti_low = -18
rti_high = 10
#sliders
RTI_slider_low = Slider(start=-30, end=70, value=-18, step=.1, title="dB low Range", width = 300)
RTI_slider_high = Slider(start=-30, end=70, value=10, step=.1, title="dB high Range", width = 300)
U_slider_low = Slider(start=-80, end=80, value=-80, step=.1, title="Eastern Wind Low Range (m/s)", width = 300)
U_slider_high = Slider(start=-80, end=80, value=80, step=.1, title="Eastern Wind High Range (m/s)", width = 300)
V_slider_low = Slider(start=-100, end=80, value=-100, step=.1, title="Northern Wind Low Range (m/s)", width = 300)
V_slider_high = Slider(start=-100, end=80, value=80, step=.1, title="Northern Wind High Range (m/s)", width = 300)
W_slider_low = Slider(start=-3, end=3, value=-3, step=.1, title="Upward Wind Low Range (m/s)", width = 300)
W_slider_high = Slider(start=-3, end=3, value=3, step=.1, title="Upward Wind High Range (m/s)", width = 300)

#tab layouts
UVW_layout = column()
RTI_layout = column()
initial_thumbnails = column()
thumbnails = column()
#Panel Button
button_layout = column()

#multi_select = MultiSelect(value=[""], options=year_menu) #multiselect button
c = 0
#Home Button
Home = CheckboxButtonGroup(labels=['Home'], active=[], width = 200)
fname = ''
