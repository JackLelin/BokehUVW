import time
import copy
import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm
from bokeh.layouts import column
from bokeh.models import LinearColorMapper, ColorBar
from bokeh.plotting import figure
from bokeh.events import Tap

from spc import showFittingSpectra

#for UVW tab, this returns three wind maps and three sliders

def UVW_plotting(carrier):
    timearray = carrier.uvw_timearray
    hts = carrier.uvw_hts

    date = carrier.yyyy + '.' + carrier.mm + '.' + carrier.dd

    #reading the user selected slider value and color
    color = carrier.UVW_color_menu.value
    U_low,U_high = carrier.U_slider.value
    V_low,V_high = carrier.V_slider.value
    W_low,W_high = carrier.W_slider.value

    #Both RTI and UVW use the same range1d for plotting, the ranges are stored in init.py and initialized in page2.py
    x_r = carrier.x_r
    y_r = carrier.y_r
    
    colormap = copy.copy(cm.get_cmap(color))
    user_palette = [mpl.colors.rgb2hex(m) for m in colormap(np.arange(colormap.N))]

    # UVW plot have different values, different high and low values, thus three different color mappers
    # each colormapper is tethered to both the actual plot and the corresponding colorbar
    # changing the colormapper will change both the 'color' of the plot and the colorbar

    u_mapper = LinearColorMapper(palette=user_palette, low=U_low, high=U_high)
    u_color_bar = ColorBar(color_mapper=u_mapper, height=110, width=25, location=(0, 0), title = 'm/s')

    v_mapper = LinearColorMapper(palette=user_palette, low=V_low, high=V_high)
    v_color_bar = ColorBar(color_mapper=v_mapper, height=110, width=25, location=(0, 0), title = 'm/s')

    w_mapper = LinearColorMapper(palette=user_palette, low=W_low, high=W_high)
    w_color_bar = ColorBar(color_mapper=w_mapper, height=110, width=25, location=(0, 0), title = 'm/s')

    def windmap_handler(event):
        # Obtain the height and time of the click location 
        cursortime = event.x*3600   #time in sec
        cursorheight = event.y      #height in km
        print('cursortime:',cursortime, 'cursorheight: ', cursorheight )
        showFittingSpectra(carrier, cursortime,cursorheight)

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

    U_plot = figure(height=200, width=605, x_range = x_r, y_range= y_r,
               tools="box_zoom,pan, reset, hover, box_zoom", toolbar_location='left', tooltips = [("x", "$x"),("y", "$y"), ("m/s", "@image")])
    V_plot = figure(height=200, width=605, x_range=x_r, y_range=y_r, tools="box_zoom", tooltips = [("x", "$x"),("y", "$y"), ("m/s", "@image")])
    W_plot = figure(height=200, width=605, x_range=x_r, y_range=y_r, tools="box_zoom", tooltips = [("x", "$x"),("y", "$y"), ("m/s", "@image")])

    #config every plot
    UVWFigureConfig(U_plot, "Eastward Wind Map ", u_color_bar)
    UVWFigureConfig(V_plot, "Northward Wind Map ", v_color_bar)
    UVWFigureConfig(W_plot, "Upward Wind Map ", w_color_bar)

    V_plot.toolbar_location = None
    W_plot.toolbar_location = None
    
    timeinterval = timearray[1:] - timearray[:-1]
    #larger than usual timeinterval indicates the start of gap
    #numpy.nonzero() gives the index of the start of gap
    gap_index = ((timeinterval / np.median(timeinterval))>1.1).nonzero()[0] # numpy.nonzero() returns a tuple
    #plus 1 gives the index of the start of each acq session
    acq_start_index = np.pad(gap_index+1,(1,1),'constant') # put 0 at the start, the start of the first acq
    acq_start_index[-1] = timearray.shape[0] # put the length of the timearray at the end, the start of the additional imaginary acq

    #load image in for u, v, w
    for (idx,idx_next) in zip(acq_start_index[:-1],acq_start_index[1:]):
        #idx is the index of current acq session
        time_start = time.gmtime(timearray[idx])
        t_start = (time_start.tm_hour*3600 + time_start.tm_min *60 + time_start.tm_sec )/3600 - 5

        #idx_next is the index of next acq session, so idx_next-1 gives the index of end of last acq session
        time_end = time.gmtime(timearray[idx_next-1]) 
        t_end = (time_end.tm_hour*3600 + time_end.tm_min *60 + time_end.tm_sec )/3600 - 5
        t_end = t_end + 24 if t_end<t_start else t_end

        #t_end the the time of last the acq, we need to add the length of one acq to get the length of acq session
        dw = t_end - t_start + np.median(timeinterval)/3600 

        h_low = min(hts) 
        h_high = max(hts)
        dh = h_high-h_low
        # print(idx,idx_next,t_start,t_end,h_high,h_low,dw,dh)

        for (UVW, mapper, plot) in zip([carrier.U,carrier.V,carrier.W],[u_mapper,v_mapper,w_mapper],[U_plot,V_plot,W_plot]):
            #differnt from RTI plot, each UVW plot has its own color mapper
            plot.image(image=[UVW[idx:idx_next,:].T], x=t_start, y=h_low, dw=dw, dh=dh, color_mapper=mapper)    

    UVW_plot = column(U_plot,V_plot,W_plot)
    
    #Defining the handler for updating the UVW sliders
    #Each slider corresponds to one colormapper
    def USlideUpdateHandler(attr, new, old):
        u_mapper.update(low=carrier.U_slider.value[0], high=carrier.U_slider.value[1])
    
    def VSlideUpdateHandler(attr, new, old):
        v_mapper.update(low=carrier.V_slider.value[0], high=carrier.V_slider.value[1])
    
    def WSlideUpdateHandler(attr, new, old):
        w_mapper.update(low=carrier.W_slider.value[0], high=carrier.W_slider.value[1])

    carrier.U_slider.on_change('value', USlideUpdateHandler)
    carrier.V_slider.on_change('value', VSlideUpdateHandler)
    carrier.W_slider.on_change('value', WSlideUpdateHandler)

    return column([UVW_plot, carrier.U_slider, carrier.V_slider, carrier.W_slider])

