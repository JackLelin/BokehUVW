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
#uvw and rti data for plots are generated in this py file
#---------------------------------------------

def windmap_handler(event):
    yyyy = date[0:4]
    mm = date[5:7]
    dd = date[8:10]
#     """Retrieve windmap data"""
#     mappath = dname + "/" + year + "/Maps/" + "windmap2_" + date + ".npz"
#     f = np.load(mappath)
#     whts = f['hts']
#     f.close()
    
    """Retrieve spc data"""
    spcpath = "/rd2/MST_ISR_EEJ_cont/processed/MST/spc/y{}/spc1min/{}.{}.{}/".format(yyyy, yyyy, mm, dd)
    fnames = sorted(glob1(spcpath,'{}.{}.{}.*.npz'.format(yyyy, mm, dd)))
    fms = [int(fname[11:13])*3600e3+int(fname[14:16])*60e3+int(fname[17:19])*1e3 for fname in fnames]
    offset = (fms[1]-fms[0])/2
    fname = fnames[np.argmin(abs(event.x*3600e3+offset-np.array(fms)))]
    f = np.load(spcpath+fname)
    spc = f['spc']
    hts = f['hts']
    vel_arr = f['vel_arr']
    f.close()
    offset = (hts[1]-hts[0])/2
    hidx = np.argmin(abs(hts+offset-event.y))
    print(spc)
    if spc.shape[2] == 64:
        spc0 = spc[0, hidx, :]
        spc1 = spc[1, hidx, :]
        spc2 = spc[2, hidx, :]
        spc3 = spc[3, hidx, :]
    else:
        spc0 = spc[0, :, hidx]
        spc1 = spc[1, :, hidx]
        spc2 = spc[2, :, hidx]
        spc3 = spc[3, :, hidx]        
    spcs = [spc0, spc1, spc2, spc3]
    
    sps = []
    for ch in range(4):
        sp = figure(plot_height=225, plot_width=350, x_range = (-12, 12), y_range=(0, 100), title='Channel {} Spectral Plot'.format(ch),toolbar_location='left')
        source = ColumnDataSource(data=dict(x=list(np.linspace(-12, 12, 64)), y=64*[0]))
        sp.line(x='x', y='y', source=source, color='black', name='line')
        sp.border_fill_color = 'white'
        sp.background_fill_color = 'white'
        sp.outline_line_color = None
        sp.grid.grid_line_color = None    
        sp.xaxis.axis_label = "Doppler speed (m/s)"
        sp.xaxis.axis_label_text_font_style = "normal"
        sps += [sp]
        sps_ids[ch] = sp.id
    #layout.children += [column(sps)]

    """Get text boxes"""
    textboxes = []
    for ch in range(4):
        textboxes += [Spacer(width=350, height=20)]
        sptext = Div(text="Time = <br> Height =")
        sptext_ids[ch] = sptext.id
        textboxes += [sptext]
        textboxes += [Spacer(width=350, height=160)]
    
def uvw_plotting(color, high_u, high_v, high_w):
    
    x_r = (5, 19)
    p = figure(plot_height=300, plot_width=700, x_range = x_r, y_range=(60, 90),
               tools='pan,wheel_zoom,box_zoom,reset,crosshair,hover', toolbar_location='left')
    p.border_fill_color = 'white'
    p.background_fill_color = 'white'
    p.outline_line_color = None
    p.grid.grid_line_color = None
    
    colormap = copy.copy(cm.get_cmap(color))
    colormap.set_bad('darkgrey')
    RdBu_r_palette = [mpl.colors.rgb2hex(m) for m in colormap(np.arange(colormap.N))]

    pmapper = LinearColorMapper(palette=RdBu_r_palette, low=-80, high=high_u)
    color_bar = ColorBar(color_mapper=pmapper, location=(0, 0), title = 'm/s')
    #p.add_layout(color_bar, 'right')

    q = figure(plot_height=300, plot_width=700, x_range=x_r, y_range=(60, 90),
               tools='pan,wheel_zoom,box_zoom,reset,crosshair,hover', toolbar_location='left')
    q.border_fill_color = 'white'
    q.background_fill_color = 'white'
    q.outline_line_color = None
    q.grid.grid_line_color = None

    colormap = copy.copy(cm.get_cmap(color))
    colormap.set_bad('darkgrey')
    RdBu_r_palette = [mpl.colors.rgb2hex(m) for m in colormap(np.arange(colormap.N))]

    qmapper = LinearColorMapper(palette=RdBu_r_palette, low=-100, high=high_v)
    color_bar = ColorBar(color_mapper=qmapper, location=(0, 0), title = 'm/s')
    #q.add_layout(color_bar, 'right')

    r = figure(plot_height=300, plot_width=700, x_range=x_r, y_range=(60, 90),
               tools='pan,wheel_zoom,box_zoom,reset,crosshair,hover', toolbar_location='left')
    r.border_fill_color = 'white'
    r.background_fill_color = 'white'
    r.outline_line_color = None
    r.grid.grid_line_color = None

    colormap = copy.copy(cm.get_cmap(color))
    colormap.set_bad('darkgrey')
    RdBu_r_palette = [mpl.colors.rgb2hex(m) for m in colormap(np.arange(colormap.N))]

    rmapper = LinearColorMapper(palette=RdBu_r_palette, low=-3, high=high_w)
    color_bar = ColorBar(color_mapper=rmapper, location=(0, 0), title = 'm/s')
    #r.add_layout(color_bar, 'right') 
    
    return p, pmapper, q, qmapper, r, rmapper

def rti_plotting(color, high):
    x_r = (5, 19)
    p = figure(plot_height=300, plot_width=700, x_range = x_r, y_range=(60, 90),
               tools='pan,wheel_zoom,box_zoom,reset,crosshair,hover', toolbar_location='left')
    p.border_fill_color = 'white'
    p.background_fill_color = 'white'
    p.outline_line_color = None
    p.grid.grid_line_color = None
    
    colormap = copy.copy(cm.get_cmap(color))
    colormap.set_bad('darkgrey')
    RdBu_r_palette = [mpl.colors.rgb2hex(m) for m in colormap(np.arange(colormap.N))]

    pmapper = LinearColorMapper(palette=RdBu_r_palette, low=-18, high=high)
    color_bar = ColorBar(color_mapper=pmapper, location=(0, 0), title = 'dB')
    p.add_layout(color_bar, 'right')

    q = figure(plot_height=300, plot_width=700, x_range=x_r, y_range=(60, 90),
               tools='pan,wheel_zoom,box_zoom,reset,crosshair,hover', toolbar_location='left')
    q.border_fill_color = 'white'
    q.background_fill_color = 'white'
    q.outline_line_color = None
    q.grid.grid_line_color = None

    colormap = copy.copy(cm.get_cmap(color))
    colormap.set_bad('darkgrey')
    RdBu_r_palette = [mpl.colors.rgb2hex(m) for m in colormap(np.arange(colormap.N))]

    qmapper = LinearColorMapper(palette=RdBu_r_palette, low=-18, high=high)
    color_bar = ColorBar(color_mapper=qmapper, location=(0, 0), title = 'dB')
    q.add_layout(color_bar, 'right')

    r = figure(plot_height=300, plot_width=700, x_range=x_r, y_range=(60, 90),
               tools='pan,wheel_zoom,box_zoom,reset,crosshair,hover', toolbar_location='left')
    r.border_fill_color = 'white'
    r.background_fill_color = 'white'
    r.outline_line_color = None
    r.grid.grid_line_color = None

    colormap = copy.copy(cm.get_cmap(color))
    colormap.set_bad('darkgrey')
    RdBu_r_palette = [mpl.colors.rgb2hex(m) for m in colormap(np.arange(colormap.N))]

    rmapper = LinearColorMapper(palette=RdBu_r_palette, low=-18, high=high)
    color_bar = ColorBar(color_mapper=rmapper, location=(0, 0), title = 'dB')
    r.add_layout(color_bar, 'right') 
    
    s = figure(plot_height=300, plot_width=700, x_range=x_r, y_range=(60, 90),
               tools='pan,wheel_zoom,box_zoom,reset,crosshair,hover', toolbar_location='left')
    s.border_fill_color = 'white'
    s.background_fill_color = 'white'
    s.outline_line_color = None
    s.grid.grid_line_color = None

    colormap = copy.copy(cm.get_cmap(color))
    colormap.set_bad('darkgrey')
    RdBu_r_palette = [mpl.colors.rgb2hex(m) for m in colormap(np.arange(colormap.N))]

    smapper = LinearColorMapper(palette=RdBu_r_palette, low=-18, high=high)
    color_bar = ColorBar(color_mapper=smapper, location=(0, 0), title = 'dB')
    s.add_layout(color_bar, 'right') 
    return p, pmapper, q, qmapper, r, rmapper, s, smapper

    