#!/raid/home/klee137/bokeh-python1/Python3.7.9 python

from random import random
from glob import glob1
import datetime

import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm

from bokeh.io import show
from bokeh.layouts import column, row, gridplot
from bokeh.models import Button, ColumnDataSource, LinearColorMapper, ColorBar, Title, Range1d
from bokeh.palettes import RdYlBu3, RdBu
from bokeh.plotting import figure, curdoc
from bokeh.models.widgets import Dropdown
from bokeh.transform import linear_cmap

# initial values
layout = row()
curdoc().add_root(layout)

dname = "/raid/MST_ISR_EEJ_cont/processed/mesosphere/fit_gg/spc1min"
years = sorted(glob1(dname, "*"))
year = "2015"
year_menu = [(year, year) for year in years]

# widgets
year_dropdown = Dropdown(label="MST years", button_type="warning", menu=year_menu)
date_dropdown = Dropdown(label="MST dates", button_type="warning")

#parameters for cosmetics initialized here
 
# plot objects p for U, q for V, r for W
p = figure(plot_height=300, plot_width=700, x_range = (5, 19), y_range=(60, 90), toolbar_location=None)
p.border_fill_color = 'white'
p.background_fill_color = 'white'
p.outline_line_color = None
p.grid.grid_line_color = None

colormap = cm.get_cmap('RdBu_r')
colormap.set_bad('darkgrey')
RdBu_r_palette = [mpl.colors.rgb2hex(m) for m in colormap(np.arange(colormap.N))]

mapper = LinearColorMapper(palette=RdBu_r_palette, low=-80, high=80)
color_bar = ColorBar(color_mapper=mapper, location=(0, 0), title = 'm/s')
p.add_layout(color_bar, 'right')

q = figure(plot_height=300, plot_width=700, x_range=(5, 19), y_range=(60, 90), toolbar_location=None)
q.border_fill_color = 'white'
q.background_fill_color = 'white'
q.outline_line_color = None
q.grid.grid_line_color = None

colormap = cm.get_cmap('RdBu_r')
colormap.set_bad('darkgrey')
RdBu_r_palette = [mpl.colors.rgb2hex(m) for m in colormap(np.arange(colormap.N))]

mapper = LinearColorMapper(palette=RdBu_r_palette, low=-100, high=80)
color_bar = ColorBar(color_mapper=mapper, location=(0, 0), title = 'm/s')
q.add_layout(color_bar, 'right')

r = figure(plot_height=300, plot_width=700, x_range=(5, 19), y_range=(60, 90), toolbar_location=None)
r.border_fill_color = 'white'
r.background_fill_color = 'white'
r.outline_line_color = None
r.grid.grid_line_color = None

colormap = cm.get_cmap('RdBu_r')
colormap.set_bad('darkgrey')
RdBu_r_palette = [mpl.colors.rgb2hex(m) for m in colormap(np.arange(colormap.N))]

mapper = LinearColorMapper(palette=RdBu_r_palette, low=-3, high=3)
color_bar = ColorBar(color_mapper=mapper, location=(0, 0), title = 'm/s')
r.add_layout(color_bar, 'right') 


def year_dropdown_handler(event):
    global year, dates
    global date_dropdown
    global rows
    year = event.item
    dates = sorted(glob1(dname+"/"+year, year+".*")) 
    rows = len(dates)
    date_menu = [(date, date) for date in dates]
    print(date_menu)
    # create and update MST dates 
    date_dropdown = Dropdown(label="MST dates", button_type="warning", menu=date_menu)
    date_dropdown.on_click(date_dropdown_handler)
    
    layout.children = row(year_dropdown, date_dropdown).children

year_dropdown.on_click(year_dropdown_handler)

def date_dropdown_handler(event):
  date_array = []
  for i in range(len(dates)):
   # print(i, '\t') 
    global date
    date = event.item
    #print(type(date))
    # update plot image
    mappath = dname + "/" + year + "/Maps/" + "windmap2_" + dates[i] + ".npz" 
    #print(dates[0], dates[1], date)  
    f = np.load(mappath)
    min_time = min(f['acqUTCtime'])
    max_time = max(f['acqUTCtime'])
    diff = max_time - min_time
    diff = int(diff/3600)  
    min_time = datetime.datetime.fromtimestamp(min_time)
    max_time = datetime.datetime.fromtimestamp(max_time)
    
    x0 = min_time.strftime("%H")
    x0 = float(x0)  
    x1 = max_time.strftime("%H")
    x1 = float(x1)
    print("Local time range: ", x0, x1) 
    h_min = min(f['hts'])
    h_max = max(f['hts'])
    h_diff = h_max - h_min
    print(h_min, h_max) 
    U = f['U']
    V = f['V'] 
    W = f['W']
    p.image(image=[U.T], x=x0, y=h_min, dw=diff, dh=h_diff, color_mapper=mapper)
    p.title.text = "Eastern Wind Map " + str(date)
    p.title.align = "center"
    p.add_layout(Title(text="Local Time(hour)", align="center"), "below")
    p.add_layout(Title(text="Height(km)", align="center"), "left")
    #p.add_layout(Title(text="m/s", align = "right"), "above") 
    q.image(image=[V.T], x=x0, y=h_min, dw=diff, dh=h_diff, color_mapper=mapper)
    q.title.text = "Northern  Wind Map " + str(date) 
    q.title.align = "center"
    q.add_layout(Title(text="Local Time(hour)", align="center"), "below")
    q.add_layout(Title(text="Height(km)", align="center"), "left")  
    r.image(image=[W.T], x=x0, y=h_min, dw=diff, dh=h_diff, color_mapper=mapper)
    r.title.text = "Upward Wind Map " + str(date) 
    r.title.align = "center" 
    r.add_layout(Title(text="Local Time(hour)", align="center"), "below")
    r.add_layout(Title(text="Height(km)", align="center"), "left")
    date_array.append([p, q, r]) 
    #layout.children = column(row(year_dropdown, date_dropdown), p, q, r).children    
  layout.children = gridplot(date_array, ncols = len(date_array)).children
 # print(len(p_array))
	#layout2.children = row(p, q).children
 # layout.children = row([p_array]).children  
  print(len(date_array)) 
# put the button and plot in a layout and add to the document
layout.children = row(year_dropdown).children
