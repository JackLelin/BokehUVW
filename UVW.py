import time
import copy
import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm
from bokeh.layouts import column, row
from bokeh.models import LinearColorMapper, ColorBar, Range1d, Range1d
from bokeh.plotting import figure
from bokeh.events import Tap
from bokeh.layouts import column
from spc import windmap_handler
import init
#for SNR tab, this returns the 4 beam plots and spcs

def UVW_plotting(U, V, W):

    date = init.yyyy + '.' + init.mm + '.' + init.dd
    
    color = init.UVW_color_menu.value
    U_low,U_high = init.U_slider.value
    V_low,V_high = init.V_slider.value
    W_low,W_high = init.W_slider.value

    dw = init.t_max - init.t_min
    dh = init.h_max - init.h_min
    x_r = Range1d(init.t_min, init.t_max)
    y_r = Range1d(init.h_min, init.h_max)
    
    p = figure(plot_height=200, plot_width=600, x_range = x_r, y_range= y_r,
               tools='box_zoom,pan, reset, hover', active_drag="box_zoom", toolbar_location='left', tooltips = [("x", "$x"),("y", "$y"), ("m/s", "@image")])
    
    #p.toolbar.active_tap = 'box_zoom'
    p.border_fill_color = 'white'
    p.background_fill_color = 'white'
    p.outline_line_color = None
    p.grid.grid_line_color = None

    colormap = copy.copy(cm.get_cmap(color))
    colormap.set_bad('darkgrey')
    RdBu_r_palette = [mpl.colors.rgb2hex(m) for m in colormap(np.arange(colormap.N))]

    pmapper = LinearColorMapper(palette=RdBu_r_palette, low=U_low, high=U_high)
    pcolor_bar = ColorBar(color_mapper=pmapper, location=(0, 0), title = 'm/s')

    q = figure(plot_height=200, plot_width=600, x_range=p.x_range, y_range=p.y_range, active_drag="box_zoom", tooltips = [("x", "$x"),("y", "$y"), ("m/s", "@image")])
    q.border_fill_color = 'white'
    q.background_fill_color = 'white'
    q.outline_line_color = None
    q.grid.grid_line_color = None

    qmapper = LinearColorMapper(palette=RdBu_r_palette, low=V_low, high=V_high)
    qcolor_bar = ColorBar(color_mapper=qmapper, location=(0, 0), title = 'm/s')

    r = figure(plot_height=200, plot_width=600, x_range=p.x_range, y_range=p.y_range, active_drag="box_zoom", tooltips = [("x", "$x"),("y", "$y"), ("m/s", "@image")])
    r.border_fill_color = 'white'
    r.background_fill_color = 'white'
    r.outline_line_color = None
    r.grid.grid_line_color = None

    rmapper = LinearColorMapper(palette=RdBu_r_palette, low=W_low, high=W_high)
    rcolor_bar = ColorBar(color_mapper=rmapper, location=(0, 0), title = 'm/s')
    
    p.image(image=[U.T], x=init.t_min, y=init.h_min, dw=dw, dh=dh, color_mapper=pmapper)
    p.title.text = "Eastward Wind Map " + date
    p.title.align = "center"
    p.xaxis.axis_label_text_font_style = "normal"
    p.xaxis.axis_label = "Local Time (hour)"
    p.yaxis.axis_label_text_font_style = "normal"
    p.yaxis.axis_label = "Height (km)"
    p.on_event(Tap, windmap_handler)
    p.add_layout(pcolor_bar, 'right')
    

    q.image(image=[V.T], x=init.t_min, y=init.h_min, dw=dw, dh=dh, color_mapper=qmapper)
    q.title.text = "Northward Wind Map " + date
    q.title.align = "center"
    q.xaxis.axis_label_text_font_style = "normal"
    q.xaxis.axis_label = "Local Time (hour)"
    q.yaxis.axis_label_text_font_style = "normal"
    q.yaxis.axis_label = "Height (km)"
    q.on_event(Tap, windmap_handler)
    q.add_layout(qcolor_bar, 'right')


    r.image(image=[W.T], x=init.t_min, y=init.h_min, dw=dw, dh=dh, color_mapper=rmapper)
    r.title.text = "Upward Wind Map " + date
    r.title.align = "center"
    r.xaxis.axis_label_text_font_style = "normal"
    r.xaxis.axis_label = "Local Time (hour)"
    r.yaxis.axis_label_text_font_style = "normal"
    r.yaxis.axis_label = "Height (km)"
    r.on_event(Tap, windmap_handler)
    r.add_layout(rcolor_bar, 'right')
    
    p.toolbar.logo = None
    q.toolbar.logo = None
    q.toolbar_location = None
    r.toolbar.logo = None
    r.toolbar_location = None

    UVW_plot = column(p, q, r)
    
    def USlideUpdateHandler(attr, new, old):
        pmapper.update(low=init.U_slider.value[0], high=init.U_slider.value[1])
    
    def VSlideUpdateHandler(attr, new, old):
        qmapper.update(low=init.V_slider.value[0], high=init.V_slider.value[1])
    
    def WSlideUpdateHandler(attr, new, old):
        rmapper.update(low=init.W_slider.value[0], high=init.W_slider.value[1])

    init.U_slider.on_change('value', USlideUpdateHandler)
    init.V_slider.on_change('value', VSlideUpdateHandler)
    init.W_slider.on_change('value', WSlideUpdateHandler)

    return UVW_plot

def UVW():
    mappath = init.wind_dir.format(init.yyyy, init.yyyy, init.mm, init.dd)

    #load data
    f = np.load(mappath)
    print("UVW path: " + mappath)
    #load maps
    U = f['U']
    V = f['V'] 
    W = f['W']
    # acqUTCtime = f['acqUTCtime']
    # t_min = time.gmtime(int(acqUTCtime[0]))
    # t_start = (t_min.tm_hour*3600 + t_min.tm_min *60 + t_min.tm_sec )/3600 - 5
    # t_max = time.gmtime(int(acqUTCtime[-1]))
    # t_end = (t_max.tm_hour*3600 + t_max.tm_min *60 + t_max.tm_sec )/3600 - 5
    # if (t_end < t_start):
    #     t_end = t_end + 24
    
    # init.t_min = t_start
    # init.t_max = t_end
    # print(t_start, t_end)
    #call the plotting function and return the layout with everything on 
    UVW_plot = UVW_plotting(U, V, W)
    UVW_layout = row([column([UVW_plot,init.U_slider, init.V_slider, init.W_slider]), column(init.sps), column(init.textboxes)])
    return UVW_layout
