from bokeh.io import curdoc
from bokeh.layouts import column, row, gridplot, Spacer
from bokeh.models import ColumnDataSource, Select, Div, CheckboxButtonGroup, RadioButtonGroup, CustomJS, Slider, Range1d, MultiSelect
import copy
import bokeh.document as document
from bokeh.models.widgets import Tabs, Panel, Dropdown
from bokeh.plotting import figure, output_file, show
from numpy.random import random, normal, lognormal
from numpy import roll,array, load
import numpy as np
from RTI import RTI
from UVW import UVW
from glob import glob1
from bokeh.models.widgets import Dropdown
from spc import spcs
import matplotlib.cm as cm
import matplotlib as mpl
import init
from glob import glob1
from thumbnail import year_images
global initial_maps
def year_select(attr, old, new): #year select call back function
    i = 0
    j = 0
    for year in years:
        if(year == str(old)[2:-2]): 
            doc.remove_root(thumbnail_layouts[i])  
        i = i + 1
    for year in years:
        if(year == str(new)[2:-2]): 
            doc.add_root(thumbnail_layouts[j])  
        j = j + 1
#This is loading the years

dname = "/rd2/MST_ISR_EEJ_cont/processed/mesosphere/fit_gg/spc1min" 
years = sorted(glob1(dname, "*"))
year_menu = [(year, year) for year in years]
thumbnail_layouts = []
for year in years:
    thumbnail_layouts.append(year_images(str(year)))
multi_select = MultiSelect(value=["2015"], options=year_menu) #multiselect button

Title_txt = Div(text = 'Mesospheric Winds at JRO', style={'font-size': '200%', 'color': 'black'}, width =1200)
Info_txt = Div(text = "This page contains a summary of the winds data measured at JRO during MST-ISR campaigns. To explore the data in an interactive mode click on the winds of the day of interest. By default the results shown are from the last analyzed year. Previous years can be selected using the drop-down list.")
init.sps, init.textboxes = spcs('')  #initialize the empty textboxes

doc = curdoc()#initializing the document
curdoc().remove_root(init.thumbnails)
doc.add_root(column(Title_txt, Info_txt)) #adding texts to the document
doc.add_root(multi_select)#adding the year selection button
initial_thumbnails = year_images(str(2015))
thumbnails = year_images(str(2015))

doc.add_root(thumbnail_layouts[-4])
#doc.add_root(year_images(str(2015)))
init.Home = CheckboxButtonGroup(labels=['Home'], active=[], width = 200)#reset of home button(shown on page2)
init.Home.js_on_click(CustomJS(args=dict(urls=['https://remote1.ece.illinois.edu/JRO/MST2uvw']),code="""window.open(urls, "_self");"""))#URL that reopens new webpage

multi_select.on_change('value', year_select)#year selection callback function

#Everything below this is a reset for all the global variables defined in init.py
init.UVW_color_menu = Select(options = init.colors, value = init.colors[0], title = 'Color', width = 500)
init.RTI_color_menu = Select(options = init.colors, value = init.colors[-2], title = 'Color', width = 500)

init.RTI_slider_low = Slider(start=-30, end=70, value=-18, step=.1, title="dB low Range", width = 300)
init.RTI_slider_high = Slider(start=-30, end=70, value=10, step=.1, title="dB high Range", width = 300)
init.U_slider_low = Slider(start=-80, end=80, value=-80, step=.1, title="Eastern Wind Low Range (m/s)", width = 300)
init.U_slider_high = Slider(start=-80, end=80, value=80, step=.1, title="Eastern Wind High Range (m/s)", width = 300)
init.V_slider_low = Slider(start=-100, end=80, value=-100, step=.1, title="Northern Wind Low Range (m/s)", width = 300)
init.V_slider_high = Slider(start=-100, end=80, value=80, step=.1, title="Northern Wind High Range (m/s)", width = 300)
init.W_slider_low = Slider(start=-3, end=3, value=-3, step=.1, title="Upward Wind Low Range (m/s)", width = 300)
init.W_slider_high = Slider(start=-3, end=3, value=3, step=.1, title="Upward Wind High Range (m/s)", width = 300)

init.g = np.load(init.dpath_snr)
acqUTCtime = init.g['acqUTCtime']
"""Change UTC to local time (Peru)."""
localTime = acqUTCtime - 5*3600
"""Constrain time to 24 hours."""
localTime = localTime % (24*3600)

init.t_min = float(min(localTime)/3600)
init.t_max = float(max(localTime)/3600)
hts = init.g['hts']
init.h_min = min(hts)
init.h_max = max(hts)
#document title 
doc.title = "New Site"

