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
from get_spc import windmap_handler
#---------------------------------------------
#uvw and rti maps are generated in this py file
#---------------------------------------------

def uvw_map(U, V, W, a, b, c, color, t_min, h_min, t_diff, h_diff, date, high_u, high_v, high_w):
    colormap = copy.copy(cm.get_cmap(color))
    colormap.set_bad('darkgrey')
    RdBu_r_palette = [mpl.colors.rgb2hex(m) for m in colormap(np.arange(colormap.N))]
    amap = LinearColorMapper(palette=RdBu_r_palette, low=-80, high=high_u)
    color_bar = ColorBar(color_mapper=amap, location=(0, 0), title = 'm/s')

    a.image(image=[U.T], x=t_min, y=h_min, dw=t_diff, dh=h_diff, color_mapper=amap)
    a.title.text = "Eastward Wind Map " + str(date)
    a.title.align = "center"
    a.xaxis.axis_label_text_font_style = "normal"
    a.xaxis.axis_label = "Local Time (hour)"
    a.yaxis.axis_label_text_font_style = "normal"
    a.yaxis.axis_label = "Height (km)"
    a.on_event(Tap, windmap_handler)
    a.add_layout(color_bar, 'right')
    
    bmap = LinearColorMapper(palette=RdBu_r_palette, low=-100, high=high_v)
    color_bar = ColorBar(color_mapper=bmap, location=(0, 0), title = 'm/s')
    b.image(image=[V.T], x=t_min, y=h_min, dw=t_diff, dh=h_diff, color_mapper=bmap)
    b.title.text = "Eastward Wind Map " + str(date)
    b.title.align = "center"
    b.xaxis.axis_label_text_font_style = "normal"
    b.xaxis.axis_label = "Local Time (hour)"
    b.yaxis.axis_label_text_font_style = "normal"
    b.yaxis.axis_label = "Height (km)"
    b.on_event(Tap, windmap_handler)
    b.add_layout(color_bar, 'right')
    cmap = LinearColorMapper(palette=RdBu_r_palette, low=-3, high=high_w)
    color_bar = ColorBar(color_mapper=cmap, location=(0, 0), title = 'm/s')
    c.image(image=[W.T], x=t_min, y=h_min, dw=t_diff, dh=h_diff, color_mapper=bmap)
    c.title.text = "Eastward Wind Map " + str(date)
    c.title.align = "center"
    c.xaxis.axis_label_text_font_style = "normal"
    c.xaxis.axis_label = "Local Time (hour)"
    c.yaxis.axis_label_text_font_style = "normal"
    c.yaxis.axis_label = "Height (km)"
    c.on_event(Tap, windmap_handler)
    c.add_layout(color_bar, 'right')
    
def rti_map(snrdB_map_ch0, snrdB_map_ch1, snrdB_map_ch2, snrdB_map_ch3, p, q, r, s, color, t_min, h_min, t_diff, h_diff, date, high):
    colormap = copy.copy(cm.get_cmap(color))
    colormap.set_bad('darkgrey')
    RdBu_r_palette = [mpl.colors.rgb2hex(m) for m in colormap(np.arange(colormap.N))]
    pmap = LinearColorMapper(palette=RdBu_r_palette, low=-18, high=high)
    #color_bar = ColorBar(color_mapper=pmap, location=(0, 0), title = 'dB')
    p.image(image=[snrdB_map_ch0.T], x=t_min, y=h_min, dw=t_diff, dh=h_diff, color_mapper=pmap)
    p.title.text = "East Beam SNR Map " + str(date)
    p.title.align = "center"
    p.xaxis.axis_label_text_font_style = "normal"
    p.xaxis.axis_label = "Local Time (hour)"
    p.yaxis.axis_label_text_font_style = "normal"
    p.yaxis.axis_label = "Height (km)"
    p.on_event(Tap, windmap_handler)
    #p.add_layout(color_bar, 'right')
    
    qmap = LinearColorMapper(palette=RdBu_r_palette, low=-18, high=high)
    color_bar = ColorBar(color_mapper=qmap, location=(0, 0), title = 'dB')
    q.image(image=[snrdB_map_ch1.T], x=t_min, y=h_min, dw=t_diff, dh=h_diff, color_mapper=qmap)
    q.title.text = "West Beam SNR Map " + str(date) 
    q.title.align = "center"
    q.xaxis.axis_label_text_font_style = "normal"
    q.xaxis.axis_label = "Local Time (hour)"
    q.yaxis.axis_label_text_font_style = "normal"
    q.yaxis.axis_label = "Height (km)"
    q.on_event(Tap, windmap_handler)
    #q.add_layout(color_bar, 'right')
    
    rmap = LinearColorMapper(palette=RdBu_r_palette, low=-18, high=high)
    color_bar = ColorBar(color_mapper=rmap, location=(0, 0), title = 'dB')
    r.image(image=[snrdB_map_ch2.T], x=t_min, y=h_min, dw=t_diff, dh=h_diff, color_mapper=rmap)
    r.title.text = "South Beam SNR Map " + str(date) 
    r.title.align = "center" 
    r.xaxis.axis_label_text_font_style = "normal"
    r.xaxis.axis_label = "Local Time (hour)"
    r.yaxis.axis_label_text_font_style = "normal"
    r.yaxis.axis_label = "Height (km)"
    r.on_event(Tap, windmap_handler)
    #r.add_layout(color_bar, 'right')
    
    s.image(image=[snrdB_map_ch3.T], x=t_min, y=h_min, dw=t_diff, dh=h_diff, color_mapper=rmap)
    s.title.text = "Vertical Beam SNR Map " + str(date) 
    s.title.align = "center" 
    s.xaxis.axis_label_text_font_style = "normal"
    s.xaxis.axis_label = "Local Time (hour)"
    s.yaxis.axis_label_text_font_style = "normal"
    s.yaxis.axis_label = "Height (km)"
    s.on_event(Tap, windmap_handler)
    #s.add_layout(color_bar, 'right')
