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
import init

"""Spectral plot model IDs."""
sps_ids = [None, None, None, None]
"""Spectral description model IDs."""
sptext_ids = [None, None, None, None]
def spcs(fname):
    channel = ['0', '1', '2', '3']
    sps = []
    for ch in range(4):
        sp = figure(plot_height=200, plot_width=300, x_range = (x_l, x_r), y_range=(y_b, y_t), 
                    title='Ch {}'.format(channel[ch]),
                    toolbar_location='left', tools='box_zoom, pan, wheel_zoom, reset')
        source = ColumnDataSource(data=dict(x=list(np.linspace(-12, 12, 64)), y=64*[0]))
        sp.line(x='x', y='y', source=source, color='blue', name='line', alpha = .5 ,line_width = 5)
        sp.circle(x='x', y='y2', source=source, color='green', name='line2')
        sp.line(x='x', y='y3', source=source, color='red', name='line3', alpha = .5, line_width = 5)
        sp.line(x='x', y='y4', source=source, color='green', name='line4')
        sp.border_fill_color = 'white'
        sp.background_fill_color = 'white'
        sp.outline_line_color = None
        sp.grid.grid_line_color = None    
        sp.xaxis.axis_label = "Doppler speed (m/s)"
        sp.xaxis.axis_label_text_font_style = "normal"
        sp.yaxis.axis_label = "PSD Magnitude"

        sps += [sp]
        sps_ids[ch] = sp.id
        sps[0].toolbar.logo = None
    for i in range(1,4):
        sps[i].toolbar.logo = None
        sps[i].toolbar_location = None
        sps[i].x_range = sps[0].x_range
    
    """Get text boxes"""
    textboxes = []
    for ch in range(4):
        textboxes += [Spacer(width=200, height=25)]
        sptext = Div(text="Time = \t Height = \t V1 = <br> S1 = \t A1 = \t p1 = <\br> V2 = \t S2 = \t A2 = \t p2 =  <br> N = ")
        sptext_ids[ch] = sptext.id
        textboxes += [sptext]
        textboxes += [Spacer(width=200, height=100)]
    return sps, textboxes


def windmap_handler(event):
    global sps_ids
    global sptext_ids
    fig = curdoc().get_model_by_id(model_id=event._model_id)
    date = fig.title.text[-10:]
    init.yyyy = date[0:4]
    init.mm = date[5:7]
    init.dd = date[8:10]
    
    yyyy = "2017"
    mm = "04"
    dd = "20"
    """Retrieve spc data"""
                      
    spcpath = "/rd2/MST_ISR_EEJ_cont/processed/MST/spc/y{}/spc1min/{}.{}.{}/".format(init.yyyy, init.yyyy, init.mm, init.dd)
    path = "/rd2/MST_ISR_EEJ_cont/processed/mesosphere/fit_gg/spc1min/{}/Maps/fitmap_{}.{}.{}.npz".format(init.yyyy, init.yyyy, init.mm, init.dd)
    fnames = sorted(glob1(spcpath,'{}.{}.{}.*.npz'.format(init.yyyy, init.mm, init.dd)))
    #gnames = sorted(glob1(path,'fit_{}.{}.{}.*.npz'.format(init.yyyy, init.mm, init.dd)))
    fms = [int(fname[11:13])*3600e3+int(fname[14:16])*60e3+int(fname[17:19])*1e3 for fname in fnames]
    #gms = [int(gname[15:17])*3600e3+int(gname[18:20])*60e3+int(gname[21:23])*1e3 for gname in gnames]
    offset = (fms[1]-fms[0])/2 
    fname = fnames[np.argmin(abs(event.x*3600e3+offset-np.array(fms)))]
    init.fname = fname
    #gname = gnames[np.argmin(abs(event.x*3600e3+offset-np.array(gms)))]
    spcfile = spcpath + fname 
    
    t_min = time.gmtime(int(init.acqUTCtime[0]))
    t_start = (t_min.tm_hour*3600 + t_min.tm_min *60 + t_min.tm_sec )/3600 - 5
    
    sec = float(spcfile[-17:-15])
    minute = float(spcfile[-20:-18])
    hour = float(spcfile[-23:-21]) - t_start
    print(hour)
    
    print(t_start)
    time1 = 3600 * hour + 60 * minute + sec
    time1 = np.floor(time1 / 60.48)
    t = int(time1) + 1
    f = np.load(spcfile)
    g = np.load(path) 
    print("spcfile: " + spcfile)
    print("fitsfile: " + path)
    lst = g.files
    '''for item in lst:
        print(item)
        print(g[item])'''
    spc = f['spc']
    #noise1=f['noise'] #from fit file
    N = g['N_map']

    hts = f['hts']
    vel_arr = f['vel_arr']
    hts = g['hts']
    lsq1 = g['lsq1_map']
    lsq2 = g['lsq2_map']
    
    N = g['N_map']
    dv = .3473
    f.close()
    offset = (hts[1]-hts[0])/2- .075
    
    hidx = np.argmin(abs(hts+offset-event.y)) 
    
    h = hidx + 400
    noise1 = N[t, :, hidx]
    if spc.shape[2] == 64:
        spc0 = spc[0, h, :]
        spc1 = spc[1, h, :]
        spc2 = spc[2, h, :]
        spc3 = spc[3, h, :]
    else:
        spc0 = spc[0, :, h]
        spc1 = spc[1, :, h]
        spc2 = spc[2, :, h]
        spc3 = spc[3, :, h]        
    spcs = [spc0, spc1, spc2, spc3]
    v1 = np.zeros(4)
    s1 = np.zeros(4)
    a1 = np.zeros(4)
    p1 = np.zeros(4)
    v2 = np.zeros(4)
    s2 = np.zeros(4)
    a2 = np.zeros(4)
    p2 = np.zeros(4)
    dx = 8
    fit = np.zeros((4, 64))
    fit2 = np.zeros((4, 64))
    vel = vel_arr
    for ch in range(4):
        if(np.isnan(noise1[ch])):
            noise1[ch] = 1
        v1[ch] = ((lsq1[t,ch, hidx, 0]-32)*.347)
        s1[ch] = (lsq1[t,ch, hidx, 1]*.347)
        a1[ch] = (lsq1[t,ch, hidx, 2]/N[t,ch, hidx])
        p1[ch] = (lsq1[t,ch, hidx, 3])
        v2[ch] = ((lsq2[t,ch, hidx, 0]-32)*.347)
        s2[ch] = (lsq2[t,ch, hidx, 1]*.347)
        a2[ch] = (lsq2[t,ch, hidx, 2]/N[t,ch, hidx])
        p2[ch] = (lsq2[t,ch, hidx, 3])
        print(v1[ch], s1[ch], a1[ch], p1[ch], v2[ch], s2[ch], a2[ch], p2[ch])
        if(np.isnan(v1[ch])):
            fit[ch, :] = 0 * np.abs(vel)
        else:
            inner = np.abs((vel - v1[ch])/s1[ch])
            inner = -.5*np.power(inner, p1[ch])
            fit[ch, :] = fit[ch, :] + a1[ch] * np.exp(inner)
        if(np.isnan(v2[ch])):
            fit2[ch, :] = 0 * np.abs(vel)
        else: 
            inner = np.abs((vel - v2[ch])/s2[ch])
            inner = -.5*np.power(inner, p2[ch])
            fit2[ch, :] = fit2[ch, :] + a2[ch] * np.exp(inner) 

    """Update spectral figure models."""
    
    for ch in range(4):
        spcfig = curdoc().get_model_by_id(model_id=sps_ids[ch])
        """Clear plot beforehand."""
        line = spcfig.select(name='line')  
        line.data_source.data['x'] = list(vel)
        line.data_source.data['y'] = list(noise1[ch]*(fit[ch, :] + 1))
        
        line2 = spcfig.select(name='line2')  
        line2.data_source.data['x'] = list(vel)
        line2.data_source.data['y2'] = list(spcs[ch])
        line3 = spcfig.select(name='line3')  
        line3.data_source.data['x'] = list(vel)
        line3.data_source.data['y3'] = list(noise1[ch]*(fit2[ch, :] + 1))
        line4 = spcfig.select(name='line4')  
        line4.data_source.data['x'] = list(vel)
        line4.data_source.data['y4'] = list(spcs[ch])
        #line4 = line4.fillna('')
        spcfig.y_range.start = 0
        spcfig.y_range.end = noise1[ch] * max(max((fit[ch, :] + 1)), max((fit2[ch, :] + 1)), max(spcs[ch]/noise1[ch]))
        
    """Update spectral texts models."""
    for ch in range(4):
        sptext = curdoc().get_model_by_id(model_id=sptext_ids[ch])
        sptext.text = "Time = {0}:{1}:{2} \t Height = {3:.2f} km <br> V1 = {4:.2f} m/s \t S1 = {5:.2f} m/s \t A1 = {6:.2f} \t p1 = {7:.2f} <br> V2 = {8:.2f} m/s \t S2 = {9:.2f} m/s \t A2 = {10:.2f} \t p2 = {11:.2f} <br> N = {12: .2f}".format(fname[11:13], fname[14:16], fname[17:19], hts[hidx], (lsq1[t, ch, hidx, 0]-32)*dv, lsq1[t, ch, hidx, 1]*dv, lsq1[t, ch, hidx, 2]/N[t, ch, hidx], lsq1[t, ch, hidx, 3], (lsq2[t, ch, hidx, 0]-32)*dv, lsq2[t, ch, hidx, 1]*dv, lsq2[t, ch, hidx, 2]/N[t, ch, hidx], lsq2[t, ch, hidx, 3], N[t, ch, hidx]/N[t, ch, hidx])
    #print(init.radio_button_group.active)
    
x_l = -12
x_r = 12
y_b = 0
y_t = 100


        
 