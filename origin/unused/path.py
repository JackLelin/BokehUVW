from random import random
from glob import glob1
import datetime
import time
import copy
import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm
from bokeh.io import show
from bokeh.layouts import column, row, gridplot, Spacer, widgetbox
from bokeh.models import Button, ColumnDataSource, LinearColorMapper, ColorBar, Title, Range1d, Div, CrosshairTool, Range1d, ColumnDataSource, Div, CheckboxButtonGroup, CustomJS, RangeSlider, TextInput, Select, Panel, Tabs, RadioButtonGroup
from bokeh.palettes import RdYlBu3, RdBu
from bokeh.plotting import figure, Figure, curdoc
from bokeh.models.widgets import Dropdown
from bokeh.transform import linear_cmap
from bokeh.events import ButtonClick, Tap, MouseEnter, MouseLeave
from bokeh.document import Document
from bokeh.core.properties import Enum
#Plotting path - get_year_images shows thumbnail of UVW maps, Then thumbnail_img_handler clears page, loads maps and spcs 
#thumbnail_img_handler calls create_fig_obj to create UVW plots on new page 
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Select, Div
from bokeh.plotting import figure, output_file, show

#---------------------------------------------
#certain data paths and initialization are done here
#---------------------------------------------

def path_init(dname, year, date):
    mappath = dname + "/" + year + "/Maps/" + "windmap2_" + date + ".npz"
    #mappath = dname + "/" + year + "/Maps/" + "fitmap_" + date + ".npz" 
    """Data paths"""
    dpath_snr = dname + "/" + year + "/Maps/fitmap_" + date + ".npz" 
    
    f = np.load(mappath)
    g = np.load(dpath_snr)
    snrdB_map = g['snrdB_map']
    snrdB_map_ch0 = snrdB_map[:, 0, :]
    snrdB_map_ch1 = snrdB_map[:, 1, :]
    snrdB_map_ch2 = snrdB_map[:, 2, :]
    snrdB_map_ch3 = snrdB_map[:, 3, :]
    
    acqUTCtime = f['acqUTCtime']
    """Change UTC to local time (Peru)."""
    localTime = acqUTCtime - 5*3600
    """Constrain time to 24 hours."""
    localTime = localTime % (24*3600)
    
    t_min = min(localTime)/3600
    t_max = max(localTime)/3600
    offset = (localTime[1]-localTime[0])/3600 - 0.297
    t_diff = t_max - t_min + offset

#     min_time = datetime.datetime.fromtimestamp(min_time)
#     max_time = datetime.datetime.fromtimestamp(max_time)
#     x0 = min_time.strftime("%H")
#     x0 = float(x0)  
#     x1 = max_time.strftime("%H")
#     x1 = float(x1)
    hts = f['hts']
    h_min = min(hts)
    h_max = max(hts)
    offset = hts[1] - hts[0] - 0.0002748959
    h_diff = h_max - h_min + offset
    U = f['U']
    V = f['V'] 
    W = f['W']
    
    return U, V, W, t_min, t_max, t_diff, hts, h_min, h_max, h_diff, snrdB_map_ch0, snrdB_map_ch1, snrdB_map_ch2, snrdB_map_ch3
    #snrdB0 = snrdB_map_ch0[t_min:t_max, h_min-offset:h_max-offset].T
    #snrdB1 = snrdB_map_ch1[ntlim0:ntlim1, y0n_1:y1n_1].T
    #snrdB2 = snrdB_map_ch2[ntlim0:ntlim1, y0n_2:y1n_2].T
    #snrdB3 = snrdB_map_ch3[ntlim0:ntlim1, y0n_3:y1n_3].T
def minipath(dname, year, date, high_u, high_v, high_w, high0, high1, high2, high3):
    mappath = dname + "/" + year + "/Maps/" + "windmap2_" + date + ".npz"
    #mappath = dname + "/" + year + "/Maps/" + "fitmap_" + date + ".npz" 
    """Data paths"""
    dpath_snr = dname + "/" + year + "/Maps/fitmap_" + date + ".npz" 
    
    f = np.load(mappath)
    g = np.load(dpath_snr)
    snrdB_map = g['snrdB_map']
    snrdB_map_ch0 = snrdB_map[:, 0, :]
    snrdB_map_ch1 = snrdB_map[:, 1, :]
    snrdB_map_ch2 = snrdB_map[:, 2, :]
    snrdB_map_ch3 = snrdB_map[:, 3, :]
    
    U = f['U'] * (high_u+80)/160
    V = f['V'] * (high_u+100)/180
    W = f['W'] * (high_u+3)/6
    #snrdB_map_ch0 = (snrdB_map_ch0 + high0) / 28
    #snrdB_map_ch1 = (snrdB_map_ch1 + high1) / 28
    #snrdB_map_ch1 = (snrdB_map_ch1 + high2) / 28
    #snrdB_map_ch1 = (snrdB_map_ch1 + high3) / 28
    
    return U, V, W, snrdB_map_ch0, snrdB_map_ch1, snrdB_map_ch2, snrdB_map_ch3