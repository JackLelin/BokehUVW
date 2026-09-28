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
from bokeh.models import Button, ColumnDataSource, LinearColorMapper, ColorBar, Title, Range1d, Div, CrosshairTool, Range1d, ColumnDataSource, Div, CheckboxButtonGroup, CustomJS, RangeSlider, TextInput, Select
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

def create_fibobj(color):
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

    pmapper = LinearColorMapper(palette=RdBu_r_palette, low=-80, high=80)
    color_bar = ColorBar(color_mapper=pmapper, location=(0, 0), title = 'm/s')
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

    qmapper = LinearColorMapper(palette=RdBu_r_palette, low=-100, high=80)
    color_bar = ColorBar(color_mapper=qmapper, location=(0, 0), title = 'm/s')
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

    rmapper = LinearColorMapper(palette=RdBu_r_palette, low=-3, high=3)
    color_bar = ColorBar(color_mapper=rmapper, location=(0, 0), title = 'm/s')
    r.add_layout(color_bar, 'right') 

    return p, pmapper, q, qmapper, r, rmapper