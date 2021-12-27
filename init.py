from bokeh.models import  Select,  RangeSlider
import numpy as np
from spc import spcs

#initializing a dummy variable date just for the webpage to run, this is changed when the user selects a year and date

dname = "/rd2/MST_ISR_EEJ_cont/processed/mesosphere/fit_gg/spc1min"
date = "2017.04.20" 
yyyy = "2017"
mm = "04"
dd = "20"

sps, textboxes = spcs('')

# years = sorted(glob1(dname, "*"))
# year_menu = [(year, year) for year in years]

#datapath load
dpath_snr = dname + "/" + yyyy + "/Maps/fitmap_" + date + ".npz" 
g = np.load(dpath_snr)
acqUTCtime = g['acqUTCtime']
"""Change UTC to local time (Peru)."""
localTime = acqUTCtime - 5*3600
"""Constrain time to 24 hours."""
localTime = localTime % (24*3600)


t_min = float(min(localTime)/3600)
t_max = float(max(localTime)/3600)
# offset = (localTime[1]-localTime[0])/3600 - 0.297
# t_diff = t_max - t_min + offset

hts = g['hts']
h_min = min(hts) - .075
h_max = max(hts) - .3 + .75
# offset = hts[1] - hts[0] - 0.0002748959
# h_diff = h_max - h_min + offset

colors = ['RdBu', 'plasma', 'viridis', 'gray', 'jet', 'RdBu_r']
 
#Colorbars value
UVW_color_menu_value = colors[0]
RTI_color_menu_value = colors[-2]


#slider range endpoints
rti_low = -18
rti_high = 10
u_low = -80
u_high = 80
v_low = -100
v_high = 80
w_low = -3
w_high = 3

#sliders_value
RTI_slider_value = (rti_low,rti_high)
U_slider_value = (u_low,u_high)
V_slider_value = (v_low,v_high)
W_slider_value = (w_low,w_high)

# RTI_slider = RangeSlider(start=rti_low, end=rti_high, value=(rti_low,rti_high), step=.1, title="dB Range", width = 300)
# U_slider = RangeSlider(start=u_low, end=u_high, value=(u_low,u_high), step=.1, title="Eastern Wind Range (m/s)", width = 300)
# V_slider = RangeSlider(start=v_low, end=v_high, value=(v_low,v_high), step=.1, title="Northern Wind Range (m/s)", width = 300)
# W_slider = RangeSlider(start=w_low, end=w_high, value=(w_low,w_high), step=.1, title="Upward Wind Range (m/s)", width = 300)


c = 0

fname = ''

