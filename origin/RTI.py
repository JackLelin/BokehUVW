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
from bokeh.models import Button, ColumnDataSource, LinearColorMapper, ColorBar, Title, Range1d, Div, CrosshairTool, Range1d, ColumnDataSource, Div, CheckboxButtonGroup, CustomJS, RangeSlider, TextInput, Select, Slider, TapTool, OpenURL
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
# global x_min, x_max, y_min, y_max

def RTI_plotting(color, date, low, high, snrdB_map_ch0, snrdB_map_ch1, snrdB_map_ch2, snrdB_map_ch3, x_min, x_max, y_min, y_max):
    def reset(): #Manual Reset
        init.t_min = 6
        init.t_max = 19
        init.h_min = 60 - .15/2 #Offset for accuracy
        init.h_max = 89.7 + .15/2 #Offset for accuracy and maxed at 89.7 for UVW(2 less pts than RTI)
        
        #Regenerate the RTI layout
        RTI_plot = RTI_plotting(color, date, low, high, snrdB_map_ch0, snrdB_map_ch1, snrdB_map_ch2, snrdB_map_ch3, x_min, x_max, init.h_min, init.h_max)
        RTI_layout = row([column([RTI_plot,  init.RTI_slider_low, init.RTI_slider_high]), column(init.sps), column(init.textboxes)])
        init.RTI_layout.children[-1:] = [column(init.button_layout, RTI_layout, init.RTI_color_menu)]
    
    #Callbacks for change in coordinate(either when user zooms or pans)
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
        init.UVW_layout = column()
        RTI_plotting(color, date, low, high, snrdB_map_ch0, snrdB_map_ch1, snrdB_map_ch2, snrdB_map_ch3, init.t_min, init.t_max, init.h_min, init.h_max)
    dw = x_max - x_min
    dh = init.h_max - init.h_min
    #initialize the parameters for the windmaps
    x_diff = x_max - x_min
    y_diff = init.h_max - init.h_min
    init.t_max = 20
    x_r = Range1d(init.t_min, init.t_max)
    y_r = Range1d(init.h_min - .075, init.h_max - .075)
    
    #p, q, r, s are the plots for the 4 RTI windmaps
    p = figure(plot_height=200, plot_width=600, x_range = x_r, y_range= y_r,
               tools='box_zoom, pan, reset, hover', active_drag="box_zoom", toolbar_location='left', tooltips = [("x", "$x"),("y", "$y"), ("SNR", "@image")]) #tooltips gives the hover details
    
    #disable the logo, make default tool as box zoom,
    p.toolbar.logo = None
    #p.toolbar.active_tap = 'box_zoom'
    p.border_fill_color = 'white'
    p.background_fill_color = 'white'
    p.outline_line_color = None
    p.grid.grid_line_color = None
    
    #make default colorbar 
    colormap = copy.copy(cm.get_cmap(color))
    colormap.set_bad('darkgrey')
    RdBu_r_palette = [mpl.colors.rgb2hex(m) for m in colormap(np.arange(colormap.N))]
    #make colorbar for p
    pmapper = LinearColorMapper(palette=RdBu_r_palette, low=low, high=high)
    color_bar = ColorBar(color_mapper=pmapper, location=(0, 0), title = 'dB')
    p.add_layout(color_bar, 'right')
    
    #q plot
    q = figure(plot_height=200, plot_width=600, x_range=p.x_range, y_range=p.y_range, active_drag="box_zoom", tooltips = [("x", "$x"),("y", "$y"), ("SNR", "@image")])
    q.border_fill_color = 'white'
    q.background_fill_color = 'white'
    q.outline_line_color = None
    q.grid.grid_line_color = None

    #colorbar for q
    qmapper = LinearColorMapper(palette=RdBu_r_palette, low=low, high=high)
    color_bar = ColorBar(color_mapper=qmapper, location=(0, 0), title = 'dB')
    q.add_layout(color_bar, 'right')
    
    #r plot
    r = figure(plot_height=200, plot_width=600, x_range=p.x_range, y_range=p.y_range, active_drag="box_zoom", tooltips = [("x", "$x"),("y", "$y"), ("SNR", "@image")])
    r.border_fill_color = 'white'
    r.background_fill_color = 'white'
    r.outline_line_color = None
    r.grid.grid_line_color = None

    #colorbar for q

    rmapper = LinearColorMapper(palette=RdBu_r_palette, low=low, high=high)
    color_bar = ColorBar(color_mapper=rmapper, location=(0, 0), title = 'dB')
    r.add_layout(color_bar, 'right') 
    
    #plot for s
    s = figure(plot_height=200, plot_width=600, x_range=p.x_range, y_range=p.y_range, active_drag="box_zoom", tooltips = [("x", "$x"),("y", "$y"), ("SNR", "@image")])
    s.border_fill_color = 'white'
    s.background_fill_color = 'white'
    s.outline_line_color = None
    s.grid.grid_line_color = None
    #colorbar for s
    smapper = LinearColorMapper(palette=RdBu_r_palette, low=low, high=high)
    color_bar = ColorBar(color_mapper=smapper, location=(0, 0), title = 'dB')
    
    #disable toolbar for q, r, s
    s.add_layout(color_bar, 'right') 
    q.toolbar.logo = None
    q.toolbar_location = None
    r.toolbar.logo = None
    r.toolbar_location = None
    s.toolbar.logo = None
    s.toolbar_location = None
    
    #load image in for p, q, r, s
    pmap = LinearColorMapper(palette=RdBu_r_palette, low=low, high=high)
    p.image(image=[snrdB_map_ch0.T], x=x_min, y=60 - .15/2, dw=dw, dh=30.15-.3, color_mapper=pmap)
    p.title.text = "East Beam SNR Map " + str(date)
    p.title.align = "center"
    p.xaxis.axis_label_text_font_style = "normal"
    p.xaxis.axis_label = "Local Time (hour)"
    p.yaxis.axis_label_text_font_style = "normal"
    p.yaxis.axis_label = "Range (km)"
    p.on_event(Tap, windmap_handler)
    
    qmap = LinearColorMapper(palette=RdBu_r_palette, low=low, high=high)
    color_bar = ColorBar(color_mapper=qmap, location=(0, 0), title = 'dB')
    q.image(image=[snrdB_map_ch1.T], x=x_min, y=60 - .15/2, dw=dw, dh=30.15-.3, color_mapper=qmap)
    q.title.text = "West Beam SNR Map " + str(date) 
    q.title.align = "center"
    q.xaxis.axis_label_text_font_style = "normal"
    q.xaxis.axis_label = "Local Time (hour)"
    q.yaxis.axis_label_text_font_style = "normal"
    q.yaxis.axis_label = "Range (km)"
    q.on_event(Tap, windmap_handler)
    
    rmap = LinearColorMapper(palette=RdBu_r_palette, low=low, high=high)
    color_bar = ColorBar(color_mapper=rmap, location=(0, 0), title = 'dB')
    r.image(image=[snrdB_map_ch2.T], x=x_min, y=60 - .15/2, dw=dw, dh=30.15-.3, color_mapper=rmap)
    r.title.text = "South Beam SNR Map " + str(date) 
    r.title.align = "center" 
    r.xaxis.axis_label_text_font_style = "normal"
    r.xaxis.axis_label = "Local Time (hour)"
    r.yaxis.axis_label_text_font_style = "normal"
    r.yaxis.axis_label = "Range (km)"
    r.on_event(Tap, windmap_handler)
    
    smap = LinearColorMapper(palette=RdBu_r_palette, low=low, high=high)
    color_bar = ColorBar(color_mapper=smap, location=(0, 0), title = 'dB')
    s.image(image=[snrdB_map_ch3.T], x=x_min, y=60 - .15/2, dw=dw, dh=30.15-.3, color_mapper=smap)
    s.title.text = "Vertical Beam SNR Map " + str(date) 
    s.title.align = "center" 
    s.xaxis.axis_label_text_font_style = "normal"
    s.xaxis.axis_label = "Local Time (hour)"
    s.yaxis.axis_label_text_font_style = "normal"
    s.yaxis.axis_label = "Range (km)"
    s.on_event(Tap, windmap_handler)
    
    #make the windmap portion of RTI layout (called RTI plot)
    RTI_plot = column(p, q, r, s)
    
    #callback for change in coordinates
    p.x_range.on_change('start', x_start)
    p.x_range.on_change('end', x_end)
    p.y_range.on_change('start', y_start)
    p.y_range.on_change('end', y_end)
    
    #callback for reset
    p.on_event('reset', reset)
 
    return RTI_plot

def RTI(dname, year, date, color, low, high):
    #load RTI datafile
    dpath_snr = dname + "/" + year + "/Maps/fitmap_" + date + ".npz"  
    g = np.load(dpath_snr)
    print("RTI path: " + dpath_snr)
    
    #load the windmaps
    snrdB_map = g['snrdB_map']
    snrdB_map_ch0 = snrdB_map[:, 0, 0:-2] #all but the last 2 entries b/c UVW is 199 entries
    snrdB_map_ch1 = snrdB_map[:, 1, 0:-2]
    snrdB_map_ch2 = snrdB_map[:, 2, 0:-2]
    snrdB_map_ch3 = snrdB_map[:, 3, 0:-2]
    acqUTCtime = g['acqUTCtime']
    init.acqUTCtime = acqUTCtime
    t_min = time.gmtime(int(acqUTCtime[0]))
    t_start = (t_min.tm_hour*3600 + t_min.tm_min *60 + t_min.tm_sec )/3600 - 5
    t_max = time.gmtime(int(acqUTCtime[-1]))
    t_end = (t_max.tm_hour*3600 + t_max.tm_min *60 + t_max.tm_sec )/3600 - 5
    if (t_end < t_start):
        t_end = t_end + 24
    
    print(t_start, t_end)
    RTI_plot = RTI_plotting(color, date, init.RTI_slider_low.value, init.RTI_slider_high.value, snrdB_map_ch0, snrdB_map_ch1, snrdB_map_ch2, snrdB_map_ch3, t_start, t_end, init.h_min, init.h_max)
    
    RTI_layout = row([column([RTI_plot, init.RTI_slider_low, init.RTI_slider_high]), column(init.sps), column(init.textboxes)])
    
    
    return RTI_layout
