from bokeh.models import  Select,  RangeSlider, Button, CustomJS
from bokeh.io import curdoc
from spc import spctraConfig

#initializing a dummy variable date just for the webpage to run, this is changed when the user selects a year and date

print('init.py was run by bokeh ***********************')
dname = "/rd2/MST_ISR_EEJ_cont/processed/mesosphere/fit_gg/spc1min"
rti_gg_files = "/rd2/MST_ISR_EEJ_cont/processed/mesosphere/fit_gg/spc1min/{}/Maps/fitmap_{}.{}.{}.npz"
wind_files = "/rd2/MST_ISR_EEJ_cont/processed/mesosphere/fit_gg/spc1min/{}/Maps/windmap2_{}.{}.{}.npz"

specs_dir = "/rd2/MST_ISR_EEJ_cont/processed/MST/spc/y{}/spc1min/{}.{}.{}/"

yyyy = "2017"
mm = "04"
dd = "20"

spectra, textboxes = spctraConfig()

t_min = 6
t_max = 19
h_min = 60 - .15/2 #Offset for accuracy
h_max = 89.7 + .15/2 #Offset for accuracy and maxed at 89.7 for UVW(2 less pts than RTI)

# The x-range and y-range Range1D object for RTI plot and UVW plot. The ranges are initialized in page2.py
# This way, the displayed range of RTI plot and UVW plot are tethered, zooming/dragging action will be synced between all plots
# Both RTI and UVW uses the same range for plotting, the ranges are stored in init.py and initialized in page2.py
x_r = None
y_r = None

colors = ['RdBu', 'plasma', 'viridis', 'gray', 'jet', 'RdBu_r']

def HomeReset(event):
    print('Button activated: resetting')
    curdoc().clear()

Home = Button(label='Home', width = 200, button_type="success")
Home.on_click(HomeReset)
Home.js_on_click(CustomJS(args=dict(urls=['https://remote1.ece.illinois.edu/JRO/MST3uvw']),code="""window.open(urls, "_self");"""))

 
#Colorbars
UVW_color_menu = Select(options = colors, value = colors[0], title = 'Color', width = 500)
RTI_color_menu = Select(options = colors, value = colors[-2], title = 'Color', width = 500)

#slider range endpoints
rti_low = -18
rti_high = 10
u_low = -80
u_high = 80
v_low = -100
v_high = 80
w_low = -3
w_high = 3

#sliders
RTI_slider = RangeSlider(start=rti_low, end=rti_high, value=(rti_low,rti_high), step=.1, title="dB Range", width = 300)
U_slider = RangeSlider(start=u_low, end=u_high, value=(u_low,u_high), step=.1, title="Eastern Wind Range (m/s)", width = 300)
V_slider = RangeSlider(start=v_low, end=v_high, value=(v_low,v_high), step=.1, title="Northern Wind Range (m/s)", width = 300)
W_slider = RangeSlider(start=w_low, end=w_high, value=(w_low,w_high), step=.1, title="Upward Wind Range (m/s)", width = 300)

c = 0

fname = ''

