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

def UVW_plotting(uvw_data):
    # load UVW
    U = uvw_data['U']
    V = uvw_data['V'] 
    W = uvw_data['W']

    timearray = uvw_data['acqUTCtime'][:,0]

    hts = uvw_data['hts']
    h_low = min(hts) - .075
    h_high = max(hts) - .3 + .75


    date = init.yyyy + '.' + init.mm + '.' + init.dd

    color = init.UVW_color_menu.value
    U_low,U_high = init.U_slider.value
    V_low,V_high = init.V_slider.value
    W_low,W_high = init.W_slider.value

    x_r = Range1d(init.t_min, init.t_max)
    y_r = Range1d(init.h_min, init.h_max)
    
    colormap = copy.copy(cm.get_cmap(color))
    colormap.set_bad('darkgrey')
    RdBu_r_palette = [mpl.colors.rgb2hex(m) for m in colormap(np.arange(colormap.N))]

    u_mapper = LinearColorMapper(palette=RdBu_r_palette, low=U_low, high=U_high)
    u_color_bar = ColorBar(color_mapper=u_mapper, location=(0, 0), title = 'm/s')

    v_mapper = LinearColorMapper(palette=RdBu_r_palette, low=V_low, high=V_high)
    v_color_bar = ColorBar(color_mapper=v_mapper, location=(0, 0), title = 'm/s')

    w_mapper = LinearColorMapper(palette=RdBu_r_palette, low=W_low, high=W_high)
    w_color_bar = ColorBar(color_mapper=w_mapper, location=(0, 0), title = 'm/s')

    def UVWFigureConfig(figname, title, c_bar):
        figname.border_fill_color = 'white'
        figname.background_fill_color = 'white'
        figname.outline_line_color = None
        figname.grid.grid_line_color = None
        figname.toolbar.logo = None
        figname.title.text = title + date
        figname.title.align = "center"
        figname.xaxis.axis_label_text_font_style = "normal"
        figname.xaxis.axis_label = "Local Time (hour)"
        figname.yaxis.axis_label_text_font_style = "normal"
        figname.yaxis.axis_label = "Height (km)"
        figname.on_event(Tap, windmap_handler)
        figname.add_layout(c_bar, 'right')

    U_plot = figure(plot_height=200, plot_width=600, x_range = x_r, y_range= y_r,
               tools='box_zoom,pan, reset, hover', active_drag="box_zoom", toolbar_location='left', tooltips = [("x", "$x"),("y", "$y"), ("m/s", "@image")])
    V_plot = figure(plot_height=200, plot_width=600, x_range=x_r, y_range=y_r, active_drag="box_zoom", tooltips = [("x", "$x"),("y", "$y"), ("m/s", "@image")])
    W_plot = figure(plot_height=200, plot_width=600, x_range=x_r, y_range=y_r, active_drag="box_zoom", tooltips = [("x", "$x"),("y", "$y"), ("m/s", "@image")])

    #config every plot
    UVWFigureConfig(U_plot, "Eastward Wind Map ", u_color_bar)
    UVWFigureConfig(V_plot, "Northward Wind Map ", v_color_bar)
    UVWFigureConfig(W_plot, "Upward Wind Map ", w_color_bar)

    V_plot.toolbar_location = None
    W_plot.toolbar_location = None
    
    timeinterval = timearray[1:] - timearray[:-1]
    #larger than usual timeinterval indicates the start gap
    #numpy.nonzero() gives the index of the start of gap
    gap_index = ((timeinterval / np.median(timeinterval))>1.1).nonzero()[0] # numpy.nonzero() returns a tuple
    #plus 1 gives the index of the start of each acq session
    acq_start_index = np.pad(gap_index+1,(1,1),'constant') # put 0 at the start and end
    
    #load image in for u, v, w
    for (idx,idx_next) in zip(acq_start_index[:-1],acq_start_index[1:]):
        if idx_next == idx+1: continue
        time_start = time.gmtime(timearray[idx])
        t_start = (time_start.tm_hour*3600 + time_start.tm_min *60 + time_start.tm_sec )/3600 - 5
        #idx_next is the index of next acq session, so idx_next-1 gives the end of last acq session
        time_end = time.gmtime(timearray[idx_next-1]) 
        t_end = (time_end.tm_hour*3600 + time_end.tm_min *60 + time_end.tm_sec )/3600 - 5
        t_end = t_end + 24 if t_end<t_start else t_end
        dw = t_end-t_start
        dh = h_high-h_low

        print(idx,idx_next,t_start,t_end,h_high,h_low,dw,dh)

        for (UVW, mapper, plot) in zip([U,V,W],[u_mapper,v_mapper,w_mapper],[U_plot,V_plot,W_plot]):
            plot.image(image=[UVW[idx:idx_next-1,:].T], x=t_start, y=h_low, dw=dw, dh=dh, color_mapper=mapper)    

    UVW_plot = column(U_plot,V_plot,W_plot)
    
    def USlideUpdateHandler(attr, new, old):
        u_mapper.update(low=init.U_slider.value[0], high=init.U_slider.value[1])
    
    def VSlideUpdateHandler(attr, new, old):
        v_mapper.update(low=init.V_slider.value[0], high=init.V_slider.value[1])
    
    def WSlideUpdateHandler(attr, new, old):
        w_mapper.update(low=init.W_slider.value[0], high=init.W_slider.value[1])

    init.U_slider.on_change('value', USlideUpdateHandler)
    init.V_slider.on_change('value', VSlideUpdateHandler)
    init.W_slider.on_change('value', WSlideUpdateHandler)

    return UVW_plot

def UVW():
    mappath = init.wind_dir.format(init.yyyy, init.yyyy, init.mm, init.dd)
    print("UVW path: " + mappath)

    #load data
    with np.load(mappath) as f:
        UVW_plot = UVW_plotting(f)

    UVW_layout = row([column([UVW_plot,init.U_slider, init.V_slider, init.W_slider]), column(init.sps), column(init.textboxes)])
    return UVW_layout
