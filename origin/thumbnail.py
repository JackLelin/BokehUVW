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
from bokeh.models import Button, ColumnDataSource, LinearColorMapper, ColorBar, Title, Range1d, Div, CrosshairTool, Range1d, ColumnDataSource, Div, CheckboxButtonGroup, CustomJS, RangeSlider, TextInput, Select, Panel, Tabs, RadioButtonGroup, Slider
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
import init
from RTI import RTI
from UVW import UVW
from page2 import page2

def thumbnail_img_effect1_handler(event): #Function that highlights black around thumbnail when mouse hovers
    fig = curdoc().get_model_by_id(model_id=event._model_id)
    print(event._model_id)
    fig.outline_line_color = 'black'
    
def thumbnail_img_effect2_handler(event): #Function that takes away that black outline when mouse leaves thumbnail
    fig = curdoc().get_model_by_id(model_id=event._model_id)
    fig.outline_line_color = None

def year_images(year): #Generating Function of thumbnails
    #doc.remove_root(init.inital_maps)
    imgs = sorted(glob1("/rd0/MST2uvw/static/thumbnail_img/y"+year+"/", '*')) 
    """Plot images of the given year"""
    #init.RTI_layout = column()
    plots = []
    for i in range(0, len(imgs)//3):
        tmaps = []
        for v in range(3):
            tmap = Figure(plot_width=350, plot_height=160,
                          title=imgs[3*i+v],
                          x_range=(0, 350), y_range=(0, 160),
                          active_drag=None,
                          toolbar_location=None)
            tmap.image_url(url=["MST2uvw/static/thumbnail_img/y"+year+"/"+imgs[3*i+v]], x=[0], y=[160],
                            w=[350], h=[160])
            tmap.grid.visible= False
            tmap.axis.visible= False
            tmap.outline_line_color = None
            tmap.title.text_font_size = '0pt'
            tmap.on_event(MouseEnter, thumbnail_img_effect1_handler)
            tmap.on_event(MouseLeave, thumbnail_img_effect2_handler)
            tmap.on_event(Tap, page2)      
            tmaps += [tmap]
        plots.append(row(tmaps))
    
    return column(plots) 
 

        
