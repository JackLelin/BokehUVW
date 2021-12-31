from bokeh.models import  Select,  RangeSlider, Button, CustomJS, Range1d
from bokeh.io import curdoc

import calendar
import numpy as np
from glob import glob1

from spc import spctraConfig
import init 

class infoCarrier(object):
    def __init__(self):
        self.yyyy = "2017"
        self.mm = "04"
        self.dd = "20"

        self.spectra, self.textboxes = spctraConfig()

        # The x-range and y-range Range1D object for RTI plot and UVW plot. The ranges are initialized in page2.py
        # This way, the displayed range of RTI plot and UVW plot are tethered, zooming/dragging action will be synced between all plots
        # Both RTI and UVW uses the same range for plotting, the ranges are stored in init.py and initialized in page2.py
        # initializing the x_range, y_range
        # Using the same Range1D objects for all plots is crucial to sync display area of all plots  
        self.x_r = Range1d(init.t_min, init.t_max)
        self.y_r = Range1d(init.h_min, init.h_max)
    
        def HomeReset(event):
            print('Button activated: resetting')
            curdoc().clear()

        self.Home = Button(label='Home', width = 200, button_type="success")
        self.Home.on_click(HomeReset)
        self.Home.js_on_click(CustomJS(args=dict(urls=[init.url]),code="""window.open(urls, "_self");"""))

 
        #Colorbars
        self.UVW_color_menu = Select(options = init.colors, value = init.colors[0], title = 'Color', width = 500)
        self.RTI_color_menu = Select(options = init.colors, value = init.colors[-2], title = 'Color', width = 500)

        #sliders
        self.RTI_slider = RangeSlider(start=init.rti_low, end=init.rti_high, value=(init.rti_low, init.rti_high), step=.1, title="dB Range", width = 300)
        self.U_slider = RangeSlider(start=init.u_low, end=init.u_high, value=(init.u_low, init.u_high), step=.1, title="Eastern Wind Range (m/s)", width = 300)
        self.V_slider = RangeSlider(start=init.v_low, end=init.v_high, value=(init.v_low, init.v_high), step=.1, title="Northern Wind Range (m/s)", width = 300)
        self.W_slider = RangeSlider(start=init.w_low, end=init.w_high, value=(init.w_low, init.w_high), step=.1, title="Upward Wind Range (m/s)", width = 300)
    
    def loadData(self):
        '''load RTI'''
        rti_gg_filename = init.rti_gg_files.format(self.yyyy, self.yyyy, self.mm, self.dd)
        print("RTI path: " + rti_gg_filename)

        # gg fit and rti map are stored in the same file
        # All gg_fit parameters are stored as map for a given day in one file
        with np.load(rti_gg_filename) as rti_gg_data:
            self.rti_gg_hts = rti_gg_data['hts']
            self.rti_gg_timearray = rti_gg_data['acqUTCtime'].flatten()

            '''For rti plot'''
            self.snrdB_map_i = rti_gg_data['snrdB_map']

            '''For spec fit'''
            # convert the UTC time to hours from 00:00 of the local time
            self.gg_LT_sec = self.rti_gg_timearray - 5*3600 - calendar.timegm((int(self.yyyy), int(self.mm), int(self.dd), 0, 0, 0))
            
            # store the gg_lsq map
            self.gg_lsq1 = rti_gg_data['lsq1_map']
            self.gg_lsq2 = rti_gg_data['lsq2_map']
            
            # store the noise map
            self.gg_noise = rti_gg_data['N_map']
        
        '''load UVW'''
        uvw_filename = init.wind_files.format(self.yyyy, self.yyyy, self.mm, self.dd)
        print("UVW path: " + uvw_filename)

        with np.load(uvw_filename) as uvw_data:
            # load UVW
            self.U = uvw_data['U']
            self.V = uvw_data['V'] 
            self.W = uvw_data['W']

            self.uvw_timearray = uvw_data['acqUTCtime'].flatten()
            self.uvw_hts = uvw_data['hts']

        '''load Spectra'''

        # Find all spectra file in the corresponding day
        self.spcpath = init.specs_dir.format(self.yyyy, self.yyyy, self.mm, self.dd)
        self.specsnames = sorted(glob1(self.spcpath,'{}.{}.{}.*.npz'.format(self.yyyy, self.mm, self.dd)))
        
        # We can obtain the time of spectra from the file name
        self.specs_time = np.array([int(fname[11:13])*3600+int(fname[14:16])*60+int(fname[17:19]) for fname in self.specsnames])