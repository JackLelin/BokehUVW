import time
import copy
import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm
from bokeh.layouts import column
from bokeh.models import  LinearColorMapper, ColorBar
from bokeh.plotting import figure
from bokeh.events import  Tap

from spc import showFittingSpectra
#for SNR tab, this returns the 4 beam plots and spcs

def RTI_plotting(carrier):
    
    #load the rti
    hts = carrier.rti_gg_hts
    timearray = carrier.rti_gg_timearray
   
    #Both RTI and UVW uses the same range for plotting, the ranges are stored in init.py and initialized in page2.py
    x_r = carrier.x_r
    y_r = carrier.y_r
    
    color = carrier.RTI_color_menu.value
    snr_low,snr_high = carrier.RTI_slider.value
      
    #make default colorbar 
    colormap = copy.copy(cm.get_cmap(color))
    colormap.set_bad('darkgrey')
    RdBu_r_palette = [mpl.colors.rgb2hex(m) for m in colormap(np.arange(colormap.N))]  
    # plot_ch0, plot_ch1, plot_ch2, plot_ch3 use the same colorbar
    c_mapper = LinearColorMapper(palette=RdBu_r_palette, low=snr_low, high=snr_high)
    color_bar = ColorBar(color_mapper=c_mapper, height=110, width=25, location=(0, 0), title = 'dB')

    #plot_ch0, plot_ch1, plot_ch2, plot_ch3 are the plots for the 4 RTI windmaps
    #disable the logo, make default tool as box zoom,
    plot_ch0 = figure(plot_height=200, plot_width=600, x_range = x_r, y_range= y_r,
                tools='box_zoom, pan, reset, hover', active_drag="box_zoom", toolbar_location='left', tooltips = [("x", "$x"),("y", "$y"), ("SNR", "@image")]) #tooltips gives the hover details
    plot_ch1 = figure(plot_height=200, plot_width=600, x_range=x_r, y_range=y_r, active_drag="box_zoom", tooltips = [("x", "$x"),("y", "$y"), ("SNR", "@image")])
    plot_ch2 = figure(plot_height=200, plot_width=600, x_range=x_r, y_range=y_r, active_drag="box_zoom", tooltips = [("x", "$x"),("y", "$y"), ("SNR", "@image")])
    plot_ch3 = figure(plot_height=200, plot_width=600, x_range=x_r, y_range=y_r, active_drag="box_zoom", tooltips = [("x", "$x"),("y", "$y"), ("SNR", "@image")])
    
    def RTI_map_handler(event):
        # Obtain the height and time of the click location 
        cursortime = event.x*3600   #time in sec
        cursorheight = event.y      #height in km
        print('cursortime:',cursortime, 'cursorheight: ', cursorheight )
        showFittingSpectra(carrier, cursortime, cursorheight)

    # defining function to initialize and config every plot
    def RTIFigureConfig(figname, title):
        figname.border_fill_color = 'white'
        figname.background_fill_color = 'white'
        figname.outline_line_color = None
        figname.grid.grid_line_color = None
        figname.toolbar.logo = None
        figname.add_layout(color_bar, 'right')
        figname.title.text = title + carrier.yyyy + '.' + carrier.mm + '.' + carrier.dd
        figname.title.align = "center"
        figname.xaxis.axis_label_text_font_style = "normal"
        figname.xaxis.axis_label = "Local Time (hour)"
        figname.yaxis.axis_label_text_font_style = "normal"
        figname.yaxis.axis_label = "Range (km)"
        figname.on_event(Tap, RTI_map_handler)

    #config every plot
    RTIFigureConfig(plot_ch0,"East Beam SNR Map ")
    RTIFigureConfig(plot_ch1,"West Beam SNR Map ")
    RTIFigureConfig(plot_ch2,"South Beam SNR Map ")
    RTIFigureConfig(plot_ch3,"Vertical Beam SNR Map ")

    #disable toolbar for q, r, s
    plot_ch1.toolbar_location = None
    plot_ch2.toolbar_location = None
    plot_ch3.toolbar_location = None
        
    def RTISlideUpdateHandler(attr, new, old):
        c_mapper.update(low=carrier.RTI_slider.value[0], high=carrier.RTI_slider.value[1])

    carrier.RTI_slider.on_change('value', RTISlideUpdateHandler)

    timeinterval = timearray[1:] - timearray[:-1]
    #larger than usual timeinterval indicates the start gap
    #numpy.nonzero() gives the index of the start of gap
    gap_index = ((timeinterval / np.median(timeinterval))>1.1).nonzero()[0] # numpy.nonzero() returns a tuple
    #plus 1 gives the index of the start of each acq session
    acq_start_index = np.pad(gap_index+1,(1,1),'constant') # put 0 at the start, the start of the first acq
    acq_start_index[-1] = timearray.shape[0] # the length of the timearray at the end, the start of the additional imaginary acq

    # The image is loaded segment by segment, for every continuous acq session
    for (idx,idx_next) in zip(acq_start_index[:-1],acq_start_index[1:]):
        #idx is the index of current acq session
        time_start = time.gmtime(timearray[idx])
        t_start = (time_start.tm_hour*3600 + time_start.tm_min *60 + time_start.tm_sec )/3600 - 5

        #idx_next is the index of next acq session, so idx_next-1 gives the index of end of last acq session
        time_end = time.gmtime(timearray[idx_next-1]) 
        t_end = (time_end.tm_hour*3600 + time_end.tm_min *60 + time_end.tm_sec )/3600 - 5
        t_end = t_end + 24 if t_end<t_start else t_end

        #t_end the the time of last the acq, we need to add the length of one acq to get the length of acq session
        dw = t_end-t_start + np.median(timeinterval)/3600 

        h_low = min(hts)
        h_high = max(hts)
        dh = h_high-h_low
        # print(idx,idx_next,t_start,t_end,h_high,h_low,dw,dh)
        
        #load image in for ch0, ch1, ch2, ch3
        for (i,plot) in zip(range(4),[plot_ch0,plot_ch1,plot_ch2,plot_ch3]):
            plot.image(image=[carrier.snrdB_map_i[idx:idx_next,i,:].T], x=t_start, y=h_low, dw=dw, dh=dh, color_mapper=c_mapper)    

    #make the windmap portion of RTI layout (called RTI plot)
    RTI_plot = column(plot_ch0, plot_ch1, plot_ch2, plot_ch3)

    return column([RTI_plot, carrier.RTI_slider])

