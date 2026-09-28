from random import random
from glob import glob1
import datetime
import time
import copy
import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm
from bokeh.io import show
from bokeh.layouts import column, row, gridplot, Spacer
from bokeh.models import Button, ColumnDataSource, LinearColorMapper, ColorBar, Title, Range1d, Div, CrosshairTool, Range1d, ColumnDataSource, Div, CheckboxButtonGroup, CustomJS, RangeSlider, TextInput, Select, Slider
from bokeh.palettes import RdYlBu3, RdBu
from bokeh.plotting import figure, Figure, curdoc
from bokeh.models.widgets import Dropdown
from bokeh.transform import linear_cmap
from bokeh.events import ButtonClick, Tap, MouseEnter, MouseLeave
from bokeh.document import Document
from bokeh.core.properties import Enum
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Select, Div
from bokeh.plotting import figure, output_file, show
from numpy.random import random, normal, lognormal
from spc import spcs, windmap_handler
import init
#for SNR tab, this returns the 4 beam plots and spcs
global x_min, x_max, y_min, y_max, x_diff, y_diff
def UVW_plotting(color, date, U_low, U_high, V_low, V_high, W_low, W_high, U, V, W, x_min, x_max, y_min, y_max):
    def reset():
        init.t_min = 6
        init.t_max = 20
        init.h_min = 60 - .15/2
        init.h_max = 89.7 + .15/2
        UVW_plot = UVW_plotting(color, date, U_low, U_high, V_low, V_high, W_low, W_high, U, V, W, x_min, x_max, init.h_min, init.h_max)
        UVW_layout = row([column([UVW_plot,  row([init.U_slider_low, init.U_slider_high]), row([init.V_slider_low, init.V_slider_high]), row([init.W_slider_low, init.W_slider_high])]), column(init.sps), column(init.textboxes)])
        
        init.UVW_layout.children[-1:] = [column(init.button_layout, UVW_layout, init.UVW_color_menu)]
    def x_start(attr, old, new):
        nonlocal x_min
        init.t_min = new
    def x_end(attr, old, new):
        nonlocal x_max
        init.t_max = new
    def y_start(attr, old, new):
        nonlocal y_min
        init.h_min = new
    def y_end(attr, old, new):
        nonlocal y_max
        init.h_max = new
        init.RTI_layout = column()
        dw = init.t_max - init.t_min
        dh = init.h_max - init.h_min
        UVW_plotting(color, date, U_low, U_high, V_low, V_high, W_low, W_high, U, V, W, x_min, x_max, y_min, y_max)
    
    dw = x_max - x_min
    y_diff = init.h_max - init.h_min
    x_r = Range1d(init.t_min, init.t_max)
    y_r = Range1d(init.h_min, init.h_max)
    
    p = figure(plot_height=200, plot_width=600, x_range = x_r, y_range= y_r,
               tools='box_zoom,pan, reset, hover', active_drag="box_zoom", toolbar_location='left', tooltips = [("x", "$x"),("y", "$y"), ("m/s", "@image")])
    p.toolbar.logo = None
    #p.toolbar.active_tap = 'box_zoom'
    p.border_fill_color = 'white'
    p.background_fill_color = 'white'
    p.outline_line_color = None
    p.grid.grid_line_color = None

    colormap = copy.copy(cm.get_cmap(color))
    colormap.set_bad('darkgrey')
    RdBu_r_palette = [mpl.colors.rgb2hex(m) for m in colormap(np.arange(colormap.N))]

    pmapper = LinearColorMapper(palette=RdBu_r_palette, low=U_low, high=U_high)
    color_bar = ColorBar(color_mapper=pmapper, location=(0, 0), title = 'dB')
    #p.add_layout(color_bar, 'right')

    q = figure(plot_height=200, plot_width=600, x_range=p.x_range, y_range=p.y_range, active_drag="box_zoom", tooltips = [("x", "$x"),("y", "$y"), ("m/s", "@image")])
    q.border_fill_color = 'white'
    q.background_fill_color = 'white'
    q.outline_line_color = None
    q.grid.grid_line_color = None

    colormap = copy.copy(cm.get_cmap(color))
    colormap.set_bad('darkgrey')
    RdBu_r_palette = [mpl.colors.rgb2hex(m) for m in colormap(np.arange(colormap.N))]

    qmapper = LinearColorMapper(palette=RdBu_r_palette, low=V_low, high=V_high)
    color_bar = ColorBar(color_mapper=qmapper, location=(0, 0), title = 'dB')
    #q.add_layout(color_bar, 'right')

    r = figure(plot_height=200, plot_width=600, x_range=p.x_range, y_range=p.y_range, active_drag="box_zoom", tooltips = [("x", "$x"),("y", "$y"), ("m/s", "@image")])
    r.border_fill_color = 'white'
    r.background_fill_color = 'white'
    r.outline_line_color = None
    r.grid.grid_line_color = None

    colormap = copy.copy(cm.get_cmap(color))
    colormap.set_bad('darkgrey')
    RdBu_r_palette = [mpl.colors.rgb2hex(m) for m in colormap(np.arange(colormap.N))]

    rmapper = LinearColorMapper(palette=RdBu_r_palette, low=W_low, high=W_high)
    color_bar = ColorBar(color_mapper=rmapper, location=(0, 0), title = 'dB')
    #r.add_layout(color_bar, 'right') 
    colormap = copy.copy(cm.get_cmap(color))
    colormap.set_bad('darkgrey')
    RdBu_r_palette = [mpl.colors.rgb2hex(m) for m in colormap(np.arange(colormap.N))]
    pmap = LinearColorMapper(palette=RdBu_r_palette, low=U_low, high=U_high)
    color_bar = ColorBar(color_mapper=pmap, location=(0, 0), title = 'm/s')
    q.toolbar.logo = None
    q.toolbar_location = None
    r.toolbar.logo = None
    r.toolbar_location = None
    
    p.image(image=[U.T], x=x_min, y=60 - .15/2, dw=dw, dh=30.15-.3, color_mapper=pmap)
    p.title.text = "Eastward Wind Map " + str(date)
    p.title.align = "center"
    p.xaxis.axis_label_text_font_style = "normal"
    p.xaxis.axis_label = "Local Time (hour)"
    p.yaxis.axis_label_text_font_style = "normal"
    p.yaxis.axis_label = "Height (km)"
    p.on_event(Tap, windmap_handler)
    p.add_layout(color_bar, 'right')
    
    qmap = LinearColorMapper(palette=RdBu_r_palette, low=V_low, high=V_high)
    color_bar = ColorBar(color_mapper=qmap, location=(0, 0), title = 'm/s')
    q.image(image=[V.T], x=x_min, y=60 - .15/2, dw=dw, dh=30.15-.3, color_mapper=qmap)
    q.title.text = "Northward Wind Map " + str(date)
    q.title.align = "center"
    q.xaxis.axis_label_text_font_style = "normal"
    q.xaxis.axis_label = "Local Time (hour)"
    q.yaxis.axis_label_text_font_style = "normal"
    q.yaxis.axis_label = "Height (km)"
    q.on_event(Tap, windmap_handler)
    q.add_layout(color_bar, 'right')
    rmap = LinearColorMapper(palette=RdBu_r_palette, low=W_low, high=W_high)
    color_bar = ColorBar(color_mapper=rmap, location=(0, 0), title = 'm/s')
    r.image(image=[W.T], x=x_min, y=60 - .15/2, dw=dw, dh=30.15-.3, color_mapper=rmap)
    r.title.text = "Upward Wind Map " + str(date)
    r.title.align = "center"
    r.xaxis.axis_label_text_font_style = "normal"
    r.xaxis.axis_label = "Local Time (hour)"
    r.yaxis.axis_label_text_font_style = "normal"
    r.yaxis.axis_label = "Height (km)"
    r.on_event(Tap, windmap_handler)
    r.add_layout(color_bar, 'right')
    
    p.on_event('reset', reset)
    UVW_plot = column(p, q, r)
    
    p.x_range.on_change('start', x_start)
    p.x_range.on_change('end', x_end)
    p.y_range.on_change('start', y_start)
    p.y_range.on_change('end', y_end)
    
    return UVW_plot

def UVW(dname, year, date, color, U_low, U_high, V_low, V_high, W_low, W_high):
    #load data
    mappath = dname + "/" + year + "/Maps/" + "windmap2_" + date + ".npz" 
    f = np.load(mappath)
    print("UVW path: " + mappath)
    #load maps
    U = f['U']
    V = f['V'] 
    W = f['W']
    acqUTCtime = f['acqUTCtime']
    t_min = time.gmtime(int(acqUTCtime[0]))
    t_start = (t_min.tm_hour*3600 + t_min.tm_min *60 + t_min.tm_sec )/3600 - 5
    t_max = time.gmtime(int(acqUTCtime[-1]))
    t_end = (t_max.tm_hour*3600 + t_max.tm_min *60 + t_max.tm_sec )/3600 - 5
    if (t_end < t_start):
        t_end = t_end + 24
    
    print(t_start, t_end)
    #call the plotting function and return the layout with everything on 
    UVW_plot = UVW_plotting(color, date, U_low, U_high, V_low, V_high, W_low, W_high, U, V, W, t_start, t_end, init.h_min, init.h_max)
    UVW_layout = row([column([UVW_plot,  row([init.U_slider_low, init.U_slider_high]), row([init.V_slider_low, init.V_slider_high]), row([init.W_slider_low, init.W_slider_high])]), column(init.sps), column(init.textboxes)])

    return UVW_layout
