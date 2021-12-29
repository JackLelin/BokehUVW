import time
import copy
import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm
from bokeh.layouts import column, row
from bokeh.models import  LinearColorMapper, ColorBar, Range1d
from bokeh.plotting import figure
from bokeh.events import  Tap

from spc import windmap_handler
import init
#for SNR tab, this returns the 4 beam plots and spcs

def RTI_plotting(snrdB_map_ch0, snrdB_map_ch1, snrdB_map_ch2, snrdB_map_ch3):
    color = init.RTI_color_menu.value
    date = init.date
    low,high = init.RTI_slider.value
    
    dw = init.t_max - init.t_min
    dh = init.h_max - init.h_min
    #initialize the parameters for the windmaps

    x_r = Range1d(init.t_min, init.t_max)
    y_r = Range1d(init.h_min - .075, init.h_max - .075)
    
    #make default colorbar 
    colormap = copy.copy(cm.get_cmap(color))
    colormap.set_bad('darkgrey')
    RdBu_r_palette = [mpl.colors.rgb2hex(m) for m in colormap(np.arange(colormap.N))]  
    #make colorbar for p
    c_mapper = LinearColorMapper(palette=RdBu_r_palette, low=low, high=high)
    color_bar = ColorBar(color_mapper=c_mapper, location=(0, 0), title = 'dB')

    #plot_ch0, plot_ch1, plot_ch2, plot_ch3 are the plots for the 4 RTI windmaps
    #disable the logo, make default tool as box zoom,
    plot_ch0 = figure(plot_height=200, plot_width=600, x_range = x_r, y_range= y_r,
                tools='box_zoom, pan, reset, hover', active_drag="box_zoom", toolbar_location='left', tooltips = [("x", "$x"),("y", "$y"), ("SNR", "@image")]) #tooltips gives the hover details
    plot_ch1 = figure(plot_height=200, plot_width=600, x_range=x_r, y_range=y_r, active_drag="box_zoom", tooltips = [("x", "$x"),("y", "$y"), ("SNR", "@image")])
    plot_ch2 = figure(plot_height=200, plot_width=600, x_range=x_r, y_range=y_r, active_drag="box_zoom", tooltips = [("x", "$x"),("y", "$y"), ("SNR", "@image")])
    plot_ch3 = figure(plot_height=200, plot_width=600, x_range=x_r, y_range=y_r, active_drag="box_zoom", tooltips = [("x", "$x"),("y", "$y"), ("SNR", "@image")])
    
    def initializeFigure(figname,title):
        figname.border_fill_color = 'white'
        figname.background_fill_color = 'white'
        figname.outline_line_color = None
        figname.grid.grid_line_color = None
        figname.add_layout(color_bar, 'right')
        figname.title.text = title + str(date)
        figname.title.align = "center"
        figname.xaxis.axis_label_text_font_style = "normal"
        figname.xaxis.axis_label = "Local Time (hour)"
        figname.yaxis.axis_label_text_font_style = "normal"
        figname.yaxis.axis_label = "Range (km)"
        figname.on_event(Tap, windmap_handler)
    #q plot
    initializeFigure(plot_ch0,"East Beam SNR Map ")
    initializeFigure(plot_ch1,"West Beam SNR Map ")
    initializeFigure(plot_ch2,"South Beam SNR Map ")
    initializeFigure(plot_ch3,"Vertical Beam SNR Map ")

    #disable toolbar for q, r, s
    plot_ch0.toolbar.logo = None
    plot_ch1.toolbar.logo = None
    plot_ch1.toolbar_location = None
    plot_ch2.toolbar.logo = None
    plot_ch2.toolbar_location = None
    plot_ch3.toolbar_location = None
    plot_ch3.toolbar.logo = None
    
    def rangeUpdateHandler(event):
        init.t_max = plot_ch0.x_range.end
        init.t_min = plot_ch0.x_range.start
        init.h_max = plot_ch0.x_range.end
        init.h_min = plot_ch0.x_range.start
    
    plot_ch0.on_event('RangesUpdate',rangeUpdateHandler)
        
    def RTISlideUpdateHandler(attr, new, old):
        c_mapper.update(low=init.RTI_slider.value[0], high=init.RTI_slider.value[1])

    init.RTI_slider.on_change('value_throttled', RTISlideUpdateHandler)

    # def plotSegments():

    #load image in for p, q, r, s
    plot_ch0.image(image=[snrdB_map_ch0.T], x=init.t_min, y=init.h_min, dw=dw, dh=dh, color_mapper=c_mapper)    
    plot_ch1.image(image=[snrdB_map_ch1.T], x=init.t_min, y=init.h_min, dw=dw, dh=dh, color_mapper=c_mapper)  
    plot_ch2.image(image=[snrdB_map_ch2.T], x=init.t_min, y=init.h_min, dw=dw, dh=dh, color_mapper=c_mapper)  
    plot_ch3.image(image=[snrdB_map_ch3.T], x=init.t_min, y=init.h_min, dw=dw, dh=dh, color_mapper=c_mapper)

    
    #make the windmap portion of RTI layout (called RTI plot)
    RTI_plot = column(plot_ch0, plot_ch1, plot_ch2, plot_ch3)

    return RTI_plot

def RTI():
    dname = init.dname
    year = init.yyyy
    date = init.date
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
    
    init.t_min = t_start
    init.t_max = t_end

    hts = g['hts']
    init.h_min = min(hts) - .075
    init.h_max = max(hts) - .3 + .75

    print(t_start, t_end)
    RTI_plot = RTI_plotting( snrdB_map_ch0, snrdB_map_ch1, snrdB_map_ch2, snrdB_map_ch3)
    RTI_layout = row([column([RTI_plot, init.RTI_slider]), column(init.sps), column(init.textboxes)])
    
    return RTI_layout
