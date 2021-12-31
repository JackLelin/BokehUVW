from glob import glob1
import calendar, time
import numpy as np
from bokeh.layouts import column, row, gridplot, Spacer, widgetbox
from bokeh.models import  ColumnDataSource, Div, CrosshairTool, Range1d, ColumnDataSource, Div
from bokeh.plotting import figure
from bokeh.io import curdoc

import init

def spctraConfig():
    channel = ['0', '1', '2', '3']
    sps = []

    for ch in range(4):
        sp = figure(plot_height=200, plot_width=300, title='Ch {}'.format(channel[ch]),
                    toolbar_location='left', tools='box_zoom, pan, wheel_zoom, reset')
        source = ColumnDataSource(data=dict(x=list(np.linspace(-12, 12, 64)), y=64*[None]))
        # line 1 and line 3 are the gg fitting
        # line 2 and line 4 are the dot and line of the data
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
        sp.yaxis.axis_label = "PSD"
        sp.toolbar.logo = None
        sp.y_range.start = 0

        sps+=[sp]
    for i in range(1,4): 
        sps[i].toolbar_location = None   #remove the toolbar for ch1, ch2, ch3
        sps[i].x_range = sps[0].x_range  #link the x_range of all sps
    
    """Get text boxes"""
    textboxes = []
    for ch in range(4):
        sptext = Div(text="V1 = <br> S1 = <br> A1 = <br> p1 = <br> V2 = <br> S2 = <br> A2 = <br> p2 =  <br> N = ", height=190)
        # textboxes += [column([Spacer(width=200, height=25), sptext, Spacer(width=200,  height=50)])]
        textboxes += [sptext]

    return sps, textboxes


def windmap_handler(event):
    #Retrieve spc data
    cursortime = event.x*3600
    cursorheight = event.y

    print('cursortime:',cursortime, 'cursorheight: ', cursorheight )
    spcpath = init.specs_dir.format(init.yyyy, init.yyyy, init.mm, init.dd)
    specsnames = sorted(glob1(spcpath,'{}.{}.{}.*.npz'.format(init.yyyy, init.mm, init.dd)))

    specs_time = np.array([int(fname[11:13])*3600+int(fname[14:16])*60+int(fname[17:19]) for fname in specsnames])
    specsname = specsnames[np.argmin(np.abs( specs_time - cursortime ))]
    specfile = spcpath + specsname
    print('specfile:', specfile)

    with np.load(specfile) as specdata:
        spec_hts = specdata['hts']
        spec_vel_array = specdata['vel_arr']
        spec_h_idx = np.argmin(np.abs(spec_hts - cursorheight))
        print('height:', spec_hts[spec_h_idx])
        spec = specdata['spc'][:,:,spec_h_idx] if specdata['spc'].shape[1] == 64 else specdata['spc'][:,spec_h_idx,:]
    
    fit_gg_file = init.rti_gg_files.format(init.yyyy, init.yyyy, init.mm, init.dd)

    with np.load(fit_gg_file) as fitggdata:
        gg_hts = fitggdata['hts']
        gg_h_idx = np.argmin(np.abs(gg_hts - cursorheight))

        # convert the UTC time to hours from 00:00 of the local time
        gg_LC_sec = fitggdata['acqUTCtime'].flatten() - 5*3600 - calendar.timegm((int(init.yyyy), int(init.mm), int(init.dd), 0, 0, 0))
        # print('gg_LC_sec', gg_LC_sec[0], 'cursortime', cursortime)
        gg_t_idx = np.argmin(np.abs(gg_LC_sec - cursortime))
        print('gg_fit_time', time.gmtime(fitggdata['acqUTCtime'].flatten()[gg_t_idx]))
        gg_lsq1 = fitggdata['lsq1_map'][gg_t_idx, :, gg_h_idx, :]
        gg_lsq2 = fitggdata['lsq2_map'][gg_t_idx, :, gg_h_idx, :]

        gg_noise = fitggdata['N_map'][gg_t_idx, :, gg_h_idx]

    print('Noise:', gg_noise)
    v1 = np.zeros(4)
    s1 = np.zeros(4)
    a1 = np.zeros(4)
    p1 = np.zeros(4)
    v2 = np.zeros(4)
    s2 = np.zeros(4)
    a2 = np.zeros(4)
    p2 = np.zeros(4)

    snr_fit1 = [None] * 4
    snr_fit2 = [None] * 4 
    snr_spec = [None] * 4

    for ch in range(4):

        v1[ch] = (gg_lsq1[ch, 0] - 32) * 0.347
        s1[ch] = gg_lsq1[ch, 1] * 0.347
        a1[ch] = gg_lsq1[ch, 2] / gg_noise[ch]
        p1[ch] = gg_lsq1[ch, 3]

        v2[ch] = (gg_lsq2[ch, 0] - 32) * 0.347
        s2[ch] = gg_lsq2[ch, 1] * 0.347
        a2[ch] = gg_lsq2[ch, 2] / gg_noise[ch]
        p2[ch] = gg_lsq2[ch, 3]

        print('Channel:', ch, 'v1=', v1[ch], 's1=', s1[ch], 'a1=', a1[ch], 'p1=', p1[ch], 
                        'v2=', v2[ch], 's2=', s2[ch], 'a2=', a2[ch], 'p2=', p2[ch])

        if(np.isnan(v1[ch]) or np.isnan(gg_noise[ch])):
            snr_fit1[ch] = np.ones_like(spec_vel_array)
        else:
            inner = np.abs((spec_vel_array - v1[ch])/s1[ch])
            snr_fit1[ch] = a1[ch] * np.exp(-.5*np.power(inner, p1[ch])) + 1

        if(np.isnan(v2[ch]) or np.isnan(gg_noise[ch])):
            snr_fit2[ch] = np.ones_like(spec_vel_array)
        else: 
            inner = np.abs((spec_vel_array - v2[ch])/s2[ch])
            snr_fit2[ch] = a2[ch] * np.exp(-.5*np.power(inner, p2[ch])) + 1

        snr_spec[ch] = spec[ch,:] / gg_noise[ch] if not np.isnan(gg_noise[ch]) else spec[ch,:] / np.max(spec[ch,:])
    
    """Update spectral figure models."""
    # line 1 and line 3 are the gg fitting
    # line 2 and line 4 are the dot and line of the data
    for ch in range(4):
        spcfig = init.spectra[ch]
        """Clear plot beforehand."""
        line = spcfig.select(name='line')  
        line.data_source.data['x'] = list(spec_vel_array)
        line.data_source.data['y'] = list(snr_fit1[ch])
        
        line2 = spcfig.select(name='line2')  
        line2.data_source.data['x'] = list(spec_vel_array)
        line2.data_source.data['y2'] = list(snr_spec[ch])

        line3 = spcfig.select(name='line3')  
        line3.data_source.data['x'] = list(spec_vel_array)
        line3.data_source.data['y3'] = list(snr_fit2[ch])

        line4 = spcfig.select(name='line4')  
        line4.data_source.data['x'] = list(spec_vel_array)
        line4.data_source.data['y4'] = list(snr_spec[ch])
        #line4 = line4.fillna('')
        spcfig.y_range.start = 0
        spcfig.y_range.end = np.max(snr_spec[ch])
        # spcfig.y_range.end = noise1[ch] * max(max((fit[ch, :] + 1)), max((fit2[ch, :] + 1)), max(spcs[ch]/noise1[ch]))
        
    """Update spectral texts models."""
    for ch in range(4):
        spec = init.spectra[ch]
        spec.title.text = 'Ch{0}, {1}:{2}:{3} LT, {4:.2f} km'.format(ch,specsname[11:13],specsname[14:16],specsname[17:19],gg_hts[gg_h_idx] )
        sptext = init.textboxes[ch]
        sptext.text = "V1 = {:.2f} m/s <br> S1 = {:.2f} <br> A1 = {:.2f} m/s <br> p1 = {:.2f} <br> V2 = {:.2f} m/s <br> S2 = {:.2f} <br> A2 = {:.2f} m/s <br> p2 = {:.2f} <br> N = {:.2f}".format(
           v1[ch], s1[ch], a1[ch], p1[ch], v2[ch], s2[ch], a2[ch], p2[ch], np.nan if np.isnan(gg_noise[ch]) else 1) # gg_noise[ch] is not used, the plot is essentially SNR
    
        
 