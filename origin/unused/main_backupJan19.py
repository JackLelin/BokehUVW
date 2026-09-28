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
from numpy.random import random, normal, lognormal
from plotting import display_num, uvw_plotting, rti_plotting
# create a Figure object
"Initialize the tabs"
layout = column()
color = 'viridis'

"""Set up year dropdown menu."""
def year_dropdown_handler(event):
    global year
    year = event.item
    get_year_images(year)
    

def fit_handler(new):
    global fit 
    fit = new.item
    print(fit)
def map_handler(new):
    global map_select 
    map_select = new.item
    print(map_select)

def my_text_input_handler(attr, old, new):
    print("Previous label: " + old)
    print("Updated label: " + new)
    
print(display_num(5, 15))
text_input = TextInput(value="default", title="Label:")
text_input.on_change("value", my_text_input_handler)

dname = "/rd2/MST_ISR_EEJ_cont/processed/mesosphere/fit_gg/spc1min"
#dname = "/rd2/MST_ISR_EEJ_cont/processed/mesosphere/fit_gg1/spc1min"
cmp = ['plasma', 'viridis', 'gray', 'jet', 'RdBu_r']
LABELS = ["jen fit", "gg fit", "gg test fit"]
years = sorted(glob1(dname, "*"))
year_menu = [(year, year) for year in years]
year_dropdown = Dropdown(label="Select the Year", button_type="success", menu=year_menu)
year_dropdown.on_click(year_dropdown_handler)

"""Texts used on webpage"""
title1 = Div(text="Mesospheric Winds at JRO", style={'font-size': '200%', 'color': 'black'}, width = 500)
title2 = Div(text="This text is suppose to be tiny")
title3 = Div(text="These buttons will be operational shortly.")
title4 = Div(text="Below are the power maps")

"""Buttons developed"""
map_options = ['SNR Map', 'Wind gg Map']
map_button_group = RadioButtonGroup(labels=map_options, active=1, width = 300)
map_button_group.js_on_click(CustomJS(code="""console.log('radio_button_group: active=' + this.active, this.toString())"""))



fit_dropdown = Dropdown(label = "Fit Options", button_type="warning", menu = LABELS)
fit_dropdown.on_click(fit_handler)

u_slider = RangeSlider(start=0, end=10, value=(1,9), step=.1, title="U Wind Limit(not operational)")
u_slider.js_on_change("value", CustomJS(code="""console.log('u_slider: value=' + this.value, this.toString())"""))
v_slider = RangeSlider(start=0, end=10, value=(1,9), step=.1, title="V Wind Limit(not operational)")
w_slider = RangeSlider(start=0, end=10, value=(1,9), step=.1, title="W Wind Limit(not operational)")

layout.children += [column([title1, title2, year_dropdown])]

"""Spectral plot model IDs."""
sps_ids = [None, None, None, None]
"""Spectral description model IDs."""
sptext_ids = [None, None, None, None]

"""Generate spectral plot based on windmap tap position."""
def windmap_handler(event):
    global sps_ids
    global sptext_ids
    fig = curdoc().get_model_by_id(model_id=event._model_id)
    date = fig.title.text[-10:]
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
    
    """Update spectral figure models."""
    for ch in range(4):
        spcfig = curdoc().get_model_by_id(model_id=sps_ids[ch])
        """Clear plot beforehand."""
        line = spcfig.select(name='line')  
        line.data_source.data['x'] = list(vel_arr)
        line.data_source.data['y'] = list(spcs[ch])
        spcfig.y_range.start = 0
        spcfig.y_range.end = max(spcs[ch])
        
    """Update spectral texts models."""
    for ch in range(4):
        sptext = curdoc().get_model_by_id(model_id=sptext_ids[ch])
        sptext.text = "Time = {0}:{1}:{2} <br> Height = {3:.2f} km".format(fname[11:13],
                                                                           fname[14:16],
                                                                           fname[17:19],
                                                                           hts[hidx])
    
"""Display windmap images from a selected year and transition to specific windmaps when selected."""
def thumbnail_img_handler(event):

    global layout1, layout2
    global sps_ids
    global sptext_ids
    fig = curdoc().get_model_by_id(model_id=event._model_id)
    date = fig.title.text[5:15]
  
    """Move to new page"""
    
    curdoc().clear()
    layout1 = row()
    layout2 = row()
    
    tab1 = Panel(child = layout, title = "Entry")
    tab2 = Panel(child = layout1, title = "RTI Maps")
    tab3 = Panel(child = layout2, title = "Wind Maps")
    tabs = Tabs(tabs=[tab2, tab3, tab1])
    curdoc().add_root(tabs)
    curdoc().add_root(layout1)
    curdoc().add_root(layout2)
    """Initialize variables"""
    mappath = dname + "/" + year + "/Maps/" + "windmap2_" + date + ".npz"
    #mappath = dname + "/" + year + "/Maps/" + "fitmap_" + date + ".npz" 
    """Data paths"""
    dpath_snr = dname + "/" + year + "/Maps/fitmap_" + date + ".npz" 
    
    f = np.load(mappath)
    g = np.load(dpath_snr)
    snrdB_map = g['snrdB_map']
    snrdB_map_ch0 = snrdB_map[:, 0, :]
    snrdB_map_ch1 = snrdB_map[:, 1, :]
    snrdB_map_ch2 = snrdB_map[:, 2, :]
    snrdB_map_ch3 = snrdB_map[:, 3, :]
    
    acqUTCtime = f['acqUTCtime']
    """Change UTC to local time (Peru)."""
    localTime = acqUTCtime - 5*3600
    """Constrain time to 24 hours."""
    localTime = localTime % (24*3600)
    
    t_min = min(localTime)/3600
    t_max = max(localTime)/3600
    offset = (localTime[1]-localTime[0])/3600 - 0.297
    t_diff = t_max - t_min + offset

#     min_time = datetime.datetime.fromtimestamp(min_time)
#     max_time = datetime.datetime.fromtimestamp(max_time)
#     x0 = min_time.strftime("%H")
#     x0 = float(x0)  
#     x1 = max_time.strftime("%H")
#     x1 = float(x1)
    hts = f['hts']
    h_min = min(hts)
    h_max = max(hts)
    offset = hts[1] - hts[0] - 0.0002748959
    h_diff = h_max - h_min + offset
    U = f['U']
    V = f['V'] 
    W = f['W']
    #snrdB0 = snrdB_map_ch0[t_min:t_max, h_min-offset:h_max-offset].T
    #snrdB1 = snrdB_map_ch1[ntlim0:ntlim1, y0n_1:y1n_1].T
    #snrdB2 = snrdB_map_ch2[ntlim0:ntlim1, y0n_2:y1n_2].T
    #snrdB3 = snrdB_map_ch3[ntlim0:ntlim1, y0n_3:y1n_3].T
    """Get windmaps"""       
    a, amap, b, bmap, c, cmap = uvw_plotting(color)
    a.image(image=[U.T], x=t_min, y=h_min, dw=t_diff, dh=h_diff, color_mapper=amap)
    a.title.text = "Eastern Wind Map " + str(date)
    a.title.align = "center"
    a.xaxis.axis_label_text_font_style = "normal"
    a.xaxis.axis_label = "Local Time (hour)"
    a.yaxis.axis_label_text_font_style = "normal"
    a.yaxis.axis_label = "Height (km)"
    a.on_event(Tap, windmap_handler)
    
    b.image(image=[V.T], x=t_min, y=h_min, dw=t_diff, dh=h_diff, color_mapper=bmap)
    b.title.text = "Northward Wind Map  " + str(date) 
    b.title.align = "center"
    b.xaxis.axis_label_text_font_style = "normal"
    b.xaxis.axis_label = "Local Time (hour)"
    b.yaxis.axis_label_text_font_style = "normal"
    b.yaxis.axis_label = "Height (km)"
    b.on_event(Tap, windmap_handler)
    
    c.image(image=[W.T], x=t_min, y=h_min, dw=t_diff, dh=h_diff, color_mapper=cmap)
    c.title.text = "Vertical Wind Map  " + str(date) 
    c.title.align = "center" 
    c.xaxis.axis_label_text_font_style = "normal"
    c.xaxis.axis_label = "Local Time (hour)"
    c.yaxis.axis_label_text_font_style = "normal"
    c.yaxis.axis_label = "Height (km)"
    c.on_event(Tap, windmap_handler)
    
    p, pmap, q, qmap, r, rmap, s, smap = rti_plotting(color)
    
    p.image(image=[snrdB_map_ch0.T], x=t_min, y=h_min, dw=t_diff, dh=h_diff, color_mapper=pmap)
    p.title.text = "East Beam SNR Map " + str(date)
    p.title.align = "center"
    p.xaxis.axis_label_text_font_style = "normal"
    p.xaxis.axis_label = "Local Time (hour)"
    p.yaxis.axis_label_text_font_style = "normal"
    p.yaxis.axis_label = "Height (km)"
    p.on_event(Tap, windmap_handler)
    
    q.image(image=[snrdB_map_ch1.T], x=t_min, y=h_min, dw=t_diff, dh=h_diff, color_mapper=qmap)
    q.title.text = "West Beam SNR Map " + str(date) 
    q.title.align = "center"
    q.xaxis.axis_label_text_font_style = "normal"
    q.xaxis.axis_label = "Local Time (hour)"
    q.yaxis.axis_label_text_font_style = "normal"
    q.yaxis.axis_label = "Height (km)"
    q.on_event(Tap, windmap_handler)
    
    r.image(image=[snrdB_map_ch2.T], x=t_min, y=h_min, dw=t_diff, dh=h_diff, color_mapper=rmap)
    r.title.text = "South Beam SNR Map " + str(date) 
    r.title.align = "center" 
    r.xaxis.axis_label_text_font_style = "normal"
    r.xaxis.axis_label = "Local Time (hour)"
    r.yaxis.axis_label_text_font_style = "normal"
    r.yaxis.axis_label = "Height (km)"
    r.on_event(Tap, windmap_handler)
    
    s.image(image=[snrdB_map_ch3.T], x=t_min, y=h_min, dw=t_diff, dh=h_diff, color_mapper=rmap)
    s.title.text = "Vertical Beam SNR Map " + str(date) 
    s.title.align = "center" 
    s.xaxis.axis_label_text_font_style = "normal"
    s.xaxis.axis_label = "Local Time (hour)"
    s.yaxis.axis_label_text_font_style = "normal"
    s.yaxis.axis_label = "Height (km)"
    s.on_event(Tap, windmap_handler)
    #layout.children += [row(column([p, q, r]))]
    
    """Get spectral plots"""
    sps = []
    for ch in range(4):
        sp = figure(plot_height=225, plot_width=350, x_range = (-12, 12), y_range=(0, 100), 
                    title='Channel {} Spectral Plot'.format(ch),
                    toolbar_location='left')
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
    color_dropdown = Select(options = cmp, value = cmp[1], title = "Color Map")
    def color_handler(attr, old, new):
    
        color = color_dropdown.value 
        
        layout1 = row()
        layout2 = row()
        tab1 = Panel(child = layout, title = "Entry")
        tab2 = Panel(child = layout1, title = "RTI Maps")
        tab3 = Panel(child = layout2, title = "Wind Maps")
        tabs = Tabs(tabs=[tab2, tab3, tab1])
        
        """Initialize variables"""
        mappath = dname + "/" + year + "/Maps/" + "windmap2_" + date + ".npz"
        #mappath = dname + "/" + year + "/Maps/" + "fitmap_" + date + ".npz" 
        """Data paths"""
        dpath_snr = dname + "/" + year + "/Maps/fitmap_" + date + ".npz" 

        f = np.load(mappath)
        g = np.load(dpath_snr)
        snrdB_map = g['snrdB_map']
        snrdB_map_ch0 = snrdB_map[:, 0, :]
        snrdB_map_ch1 = snrdB_map[:, 1, :]
        snrdB_map_ch2 = snrdB_map[:, 2, :]
        snrdB_map_ch3 = snrdB_map[:, 3, :]


        acqUTCtime = f['acqUTCtime']
        """Change UTC to local time (Peru)."""
        localTime = acqUTCtime - 5*3600
        """Constrain time to 24 hours."""
        localTime = localTime % (24*3600)

        t_min = min(localTime)/3600
        t_max = max(localTime)/3600
        offset = (localTime[1]-localTime[0])/3600 - 0.297
        t_diff = t_max - t_min + offset

    #     min_time = datetime.datetime.fromtimestamp(min_time)
    #     max_time = datetime.datetime.fromtimestamp(max_time)
    #     x0 = min_time.strftime("%H")
    #     x0 = float(x0)  
    #     x1 = max_time.strftime("%H")
    #     x1 = float(x1)
        hts = f['hts']
        h_min = min(hts)
        h_max = max(hts)
        offset = hts[1] - hts[0] - 0.0002748959
        h_diff = h_max - h_min + offset
        U = f['U']
        V = f['V'] 
        W = f['W']
        #snrdB0 = snrdB_map_ch0[t_min:t_max, h_min-offset:h_max-offset].T
        #snrdB1 = snrdB_map_ch1[ntlim0:ntlim1, y0n_1:y1n_1].T
        #snrdB2 = snrdB_map_ch2[ntlim0:ntlim1, y0n_2:y1n_2].T
        #snrdB3 = snrdB_map_ch3[ntlim0:ntlim1, y0n_3:y1n_3].T
        """Get windmaps"""  
        a, amap, b, bmap, c, cmap = uvw_plotting(color)
        a.image(image=[U.T], x=t_min, y=h_min, dw=t_diff, dh=h_diff, color_mapper=amap)
        a.title.text = "Eastward Wind Map " + str(date)
        a.title.align = "center"
        a.xaxis.axis_label_text_font_style = "normal"
        a.xaxis.axis_label = "Local Time (hour)"
        a.yaxis.axis_label_text_font_style = "normal"
        a.yaxis.axis_label = "Height (km)"
        a.on_event(Tap, windmap_handler)

        b.image(image=[V.T], x=t_min, y=h_min, dw=t_diff, dh=h_diff, color_mapper=bmap)
        b.title.text = "Northward Wind Map " + str(date) 
        b.title.align = "center"
        b.xaxis.axis_label_text_font_style = "normal"
        b.xaxis.axis_label = "Local Time (hour)"
        b.yaxis.axis_label_text_font_style = "normal"
        b.yaxis.axis_label = "Height (km)"
        b.on_event(Tap, windmap_handler)

        c.image(image=[W.T], x=t_min, y=h_min, dw=t_diff, dh=h_diff, color_mapper=cmap)
        c.title.text = "Vertical Wind Map " + str(date) 
        c.title.align = "center" 
        c.xaxis.axis_label_text_font_style = "normal"
        c.xaxis.axis_label = "Local Time (hour)"
        c.yaxis.axis_label_text_font_style = "normal"
        c.yaxis.axis_label = "Height (km)"
        c.on_event(Tap, windmap_handler)
        p, pmap, q, qmap, r, rmap, s, smap = rti_plotting(color)
        
        p.image(image=[snrdB_map_ch0.T], x=t_min, y=h_min, dw=t_diff, dh=h_diff, color_mapper=pmap)
        p.title.text = "East Beam SNR Map " + str(date)
        p.title.align = "center"
        p.xaxis.axis_label_text_font_style = "normal"
        p.xaxis.axis_label = "Local Time (hour)"
        p.yaxis.axis_label_text_font_style = "normal"
        p.yaxis.axis_label = "Height (km)"
        p.on_event(Tap, windmap_handler)

        q.image(image=[snrdB_map_ch1.T], x=t_min, y=h_min, dw=t_diff, dh=h_diff, color_mapper=qmap)
        q.title.text = "West Beam SNR Map " + str(date) 
        q.title.align = "center"
        q.xaxis.axis_label_text_font_style = "normal"
        q.xaxis.axis_label = "Local Time (hour)"
        q.yaxis.axis_label_text_font_style = "normal"
        q.yaxis.axis_label = "Height (km)"
        q.on_event(Tap, windmap_handler)

        r.image(image=[snrdB_map_ch2.T], x=t_min, y=h_min, dw=t_diff, dh=h_diff, color_mapper=rmap)
        r.title.text = "South Beam SNR Map " + str(date) 
        r.title.align = "center" 
        r.xaxis.axis_label_text_font_style = "normal"
        r.xaxis.axis_label = "Local Time (hour)"
        r.yaxis.axis_label_text_font_style = "normal"
        r.yaxis.axis_label = "Height (km)"
        r.on_event(Tap, windmap_handler)
        
        s.image(image=[snrdB_map_ch3.T], x=t_min, y=h_min, dw=t_diff, dh=h_diff, color_mapper=rmap)
        s.title.text = "Vertical Beam Map " + str(date) 
        s.title.align = "center" 
        s.xaxis.axis_label_text_font_style = "normal"
        s.xaxis.axis_label = "Local Time (hour)"
        s.yaxis.axis_label_text_font_style = "normal"
        s.yaxis.axis_label = "Height (km)"
        s.on_event(Tap, windmap_handler)
        #layout.children += [row(column([p, q, r]))]

        """Get spectral plots"""
        sps = []
        for ch in range(4):
            sp = figure(plot_height=225, plot_width=350, x_range = (-12, 12), y_range=(0, 100), 
                        title='Channel {} Spectral Plot'.format(ch),
                        toolbar_location='left')
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
        nonlocal tnow
        
        if type(new) != int:    
            curdoc().clear()
            print("curdoc clear")
            
        else:
            tnow=new
        btts = row([color_dropdown, fit_dropdown])
        tmp = row([column([p, u_slider, q, v_slider, r, w_slider, s]), column(sps), column(textboxes)])
        tmp2 = row([column([a, u_slider, b, v_slider, c, w_slider]), column(sps), column(textboxes)])
        
        tabs = Tabs(tabs=[tab2, tab3, tab1], active = tnow)

        curdoc().add_root(tabs)
        tabs.on_change('active', color_handler) 
        layout1.children += [column(title3, btts, tmp)]
        layout2.children += [column(title3, btts, tmp2)]
    tnow = 0
    
    color_dropdown.on_change('value', color_handler)
    btts = row([color_dropdown, fit_dropdown])
    tmp = row([column([p, u_slider, q, v_slider, r, w_slider, s]), column(sps), column(textboxes)])
    tmp2 = row([column([a, u_slider, b, v_slider, c, w_slider]), column(sps), column(textboxes)])
    layout1.children += [column(title3, btts, tmp)]
    layout2.children += [column(title3, btts, tmp2)]
    
def thumbnail_img_effect1_handler(event):
    fig = curdoc().get_model_by_id(model_id=event._model_id)
    fig.outline_line_color = 'black'
    
def thumbnail_img_effect2_handler(event):
    fig = curdoc().get_model_by_id(model_id=event._model_id)
    fig.outline_line_color = None
    
def get_year_images(year):
    global layout
    imgs = sorted(glob1("/rd0/MST2uvw/static/thumbnail_img/y"+year+"/", '*')) 
    """Plot images of the given year"""
    for i in range(len(imgs)//3):
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
            tmap.on_event(Tap, thumbnail_img_handler)      
            tmaps += [tmap]
             
        layout.children[i+1] = row(tmaps)
    """Remove images of the past year"""
    for i in range(len(imgs)//3, 30):
        layout.children[i] = row(3*[Spacer(width=350, height=160)])

#layout.children += [row(year_dropdown)]
for filler in range(30):
    layout.children += [row([Spacer(width=350, height=160),
                             Spacer(width=350, height=160),
                             Spacer(width=350, height=160)])]
    
curdoc().add_root(layout)
