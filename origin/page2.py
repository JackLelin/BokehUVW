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
from bokeh.models import Button, ColumnDataSource, LinearColorMapper, ColorBar, Title, Range1d, Div, CrosshairTool, Range1d, ColumnDataSource, Div, CheckboxButtonGroup, CustomJS, RangeSlider, TextInput, Select, Panel, Tabs, RadioButtonGroup, Slider, OpenURL, TapTool
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
import init
from RTI import RTI
from UVW import UVW

def page2(event):
    global sps_ids 
    global sptext_ids
     #reset home button
    
    sps_ids = [None, None, None, None]
    sptext_ids = [None, None, None, None]
    fig = curdoc().get_model_by_id(model_id=event._model_id) #extract user selection
    if (fig == None):
        init.Home.js_on_click(CustomJS(args=dict(urls=['https://remote1.ece.illinois.edu/JRO/MST2uvw']),code="""window.open(urls, "_self");"""))
    #get date info from user's selection
    init.date = fig.title.text[5:15]
    init.yyyy = init.date[0:4]
    init.mm = init.date[5:7]
    init.dd = init.date[8:10]
    
    Home = init.Home #duplicate home button to reduce chance of doubling
    LABELS = ["RTI", "UVW"] #Add additional buttons here
    Panels = RadioButtonGroup(labels=LABELS, active=0, width = 400)
    button_layout = row(Home, Panels)
    init.button_layout = button_layout
    
    #initialize local layouts to reduce chance of doubling
    RTI_layout = column()
    UVW_layout = column()
    
    #RTI Layout
    data_layout = RTI(init.dname, init.yyyy, init.date, init.RTI_color_menu.value, init.RTI_slider_low.value, init.RTI_slider_high.value)
    RTI_page = column(data_layout)
    RTI_layout.children[-1:] = [column(button_layout, RTI_page, init.RTI_color_menu)]
    init.RTI_layout = RTI_layout
    
    #Home Button Callback
    init.Home.js_on_click(CustomJS(args=dict(urls=['https://remote1.ece.illinois.edu/JRO/MST2uvw']),code="""window.open(urls, "_self");"""))
    
    #UVW Layout
    data_layout = UVW(init.dname, init.yyyy, init.date, init.UVW_color_menu.value, init.U_slider_low.value, init.U_slider_high.value, init.V_slider_low.value, init.V_slider_high.value, init.W_slider_low.value, init.W_slider_high.value)
    UVW_page = column(data_layout)
    UVW_layout.children[-1:] = [column(button_layout, UVW_page, init.UVW_color_menu)]
    
    #Clear current document and add page2 w/RTI Tab
    curdoc().clear()
    page2_doc = curdoc()
    page2_doc.add_root(init.RTI_layout)
    
    def button_cb(attr, new, old):
        
        if(Panels.active == 1): #This if block loads UVW layout and removes RTI
            data_layout = UVW(init.dname, init.yyyy, init.date, init.UVW_color_menu.value, init.U_slider_low.value, init.U_slider_high.value, init.V_slider_low.value, init.V_slider_high.value, init.W_slider_low.value, init.W_slider_high.value)
            UVW_page = column(data_layout)
            UVW_layout.children[-1:] = [column(button_layout, UVW_page, init.UVW_color_menu)]
            init.UVW_layout = UVW_layout
            page2_doc.add_root(init.UVW_layout)
            page2_doc.remove_root(init.RTI_layout)
        
        elif(Panels.active == 0): #This elif block loads RTI and removes UVW
            data_layout = RTI(init.dname, init.yyyy, init.date, init.RTI_color_menu.value, init.RTI_slider_low.value, init.RTI_slider_high.value)
            RTI_page = column(data_layout)
            init.RTI_layout.children[-1:] = [column(button_layout, RTI_page, init.RTI_color_menu)]
            page2_doc.add_root(init.RTI_layout)
            page2_doc.remove_root(init.UVW_layout)
    
    def plot_callback(attr, new, old):
        
        #Reload both tabs based on a change in slider or colorbar value
        data_layout = RTI(init.dname, init.yyyy, init.date, init.RTI_color_menu.value, init.RTI_slider_low.value, init.RTI_slider_high.value)
        RTI_page = column(data_layout)
        init.RTI_layout.children[-1:] = [column(button_layout, RTI_page, init.RTI_color_menu)]
        
        data_layout = UVW(init.dname, init.yyyy, init.date, init.UVW_color_menu.value, init.U_slider_low.value, init.U_slider_high.value, init.V_slider_low.value, init.V_slider_high.value, init.W_slider_low.value, init.W_slider_high.value)
        UVW_page = column(data_layout)
        init.UVW_layout.children[-1:] = [column(button_layout, UVW_page, init.UVW_color_menu)]
    
    #Callbacks to changes in color menu or slider
    init.RTI_slider_low.on_change('value', plot_callback)
    init.RTI_slider_high.on_change('value', plot_callback)
    
    init.RTI_color_menu.on_change('value', plot_callback)
    init.UVW_color_menu.on_change('value', plot_callback)
    
    init.U_slider_low.on_change('value', plot_callback)
    init.V_slider_low.on_change('value', plot_callback)
    init.W_slider_low.on_change('value', plot_callback)
    init.U_slider_high.on_change('value', plot_callback)
    init.V_slider_high.on_change('value', plot_callback)
    init.W_slider_high.on_change('value', plot_callback)
    
    Panels.on_change('active', button_cb)

        
