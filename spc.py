import time
import numpy as np
from bokeh.models import  ColumnDataSource, Div
from bokeh.plotting import figure

def spctraConfig():
    # This function initialize four Figures and fout textboxes 
    channel = ['0', '1', '2', '3']
    sps = []

    for ch in range(4):
        sp = figure(height=200, width=300, title='Ch {}'.format(channel[ch]),
                    toolbar_location='left', tools='box_zoom, pan, wheel_zoom, reset')
        source = ColumnDataSource(data=dict(x=list(np.linspace(-12, 12, 64)), y=64*[None]))
        # line 1 and line 3 are the gg fitting
        # line 2 and line 4 are the dot and line of the data
        sp.line(x='x', y='y', source=source, color='blue', name='line', alpha = .5 ,line_width = 5)
        sp.scatter(x='x', y='y2', size=4, source=source, color='green', name='line2')
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
        sptext = Div(text=u"V\u2081 = <br> S\u2081 = <br> A\u2081 = <br> p\u2081 = <br> V\u2082 = <br> S\u2082 = <br> A\u2082 = <br> p\u2082 =  <br> N = ",
                     height=190,
                     styles={"font-family":"Roman"})
        # textboxes += [column([Spacer(width=200, height=25), sptext, Spacer(width=200,  height=50)])]
        textboxes += [sptext]

    return sps, textboxes


def showFittingSpectra(carrier, cursortime, cursorheight):
    
    """Retrieve spc data"""
    # Picking the correct file by time
    specsname = carrier.specsnames[np.argmin(np.abs( carrier.specs_time - cursortime ))]
    specfile = carrier.spcpath + specsname
    print('specfile:', specfile)

    # Loading the spectrogram data
    with np.load(specfile) as specdata:
        spec_hts = specdata['hts']
        spec_vel_array = specdata['vel_arr']
        # Picking the correct h_idx by height
        spec_h_idx = np.argmin(np.abs(spec_hts - cursorheight))
        print('height:', spec_hts[spec_h_idx])
        # Indexing the spectra data
        spec = specdata['spc'][:,:,spec_h_idx] if specdata['spc'].shape[1] == 64 else specdata['spc'][:,spec_h_idx,:]
        npts = spec_vel_array.shape[0] #number of fft points

    """Retrieve gg_fit parameters"""
    # All gg_fit parameters are stored as map for a given day in one file
    gg_hts = carrier.rti_gg_hts
    gg_h_idx = np.argmin(np.abs(gg_hts - cursorheight))

    gg_t_idx = np.argmin(np.abs(carrier.gg_LT_sec - cursortime))
    print('gg_fit_time', time.gmtime(carrier.rti_gg_timearray[gg_t_idx]))

    # Using the t_idx and h_idx we obtain least_square_1 and least_square_2 and noise
    gg_lsq1 = carrier.gg_lsq1[gg_t_idx, :, gg_h_idx, :]
    gg_lsq2 = carrier.gg_lsq2[gg_t_idx, :, gg_h_idx, :]

    gg_noise = carrier.gg_noise[gg_t_idx, :, gg_h_idx]

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

    # Generalized gaussian function
    def gg_func(vel, V, S, A, P):
        return A * np.exp(-.5*np.power(np.abs((vel - V)/S), P))

    # Generalized gaussian function with aliasing 
    def gg_alias_func(vel, V, S, A, P):
        dv = vel[1] - vel[0]
        return gg_func(vel - npts*dv, V, S, A, P) + gg_func(vel, V, S, A, P) + gg_func(vel + npts*dv, V, S, A, P)
 
 
    for ch in range(4):
        # The parameters of two generalized gaussian 
        v1[ch] = (gg_lsq1[ch, 0] / (npts/2) - 1) * np.abs(spec_vel_array[0])
        s1[ch] = gg_lsq1[ch, 1] / (npts/2) * np.abs(spec_vel_array[0])
        a1[ch] = gg_lsq1[ch, 2] / gg_noise[ch] # plotting SNR
        p1[ch] = gg_lsq1[ch, 3]

        v2[ch] = (gg_lsq2[ch, 0] / (npts/2) - 1) * np.abs(spec_vel_array[0])
        s2[ch] = gg_lsq2[ch, 1] / (npts/2) * np.abs(spec_vel_array[0])
        a2[ch] = gg_lsq2[ch, 2] / gg_noise[ch] # plotting SNR
        p2[ch] = gg_lsq2[ch, 3]

        print('Channel:', ch, 'v1=', v1[ch], 's1=', s1[ch], 'a1=', a1[ch], 'p1=', p1[ch], 
                              'v2=', v2[ch], 's2=', s2[ch], 'a2=', a2[ch], 'p2=', p2[ch])

        if(np.isnan(v1[ch]) or np.isnan(gg_noise[ch])):
            snr_fit1[ch] = np.ones_like(spec_vel_array)
        else:
            snr_fit1[ch] = 1 + gg_alias_func(spec_vel_array, v1[ch], s1[ch], a1[ch], p1[ch])

        if(np.isnan(v2[ch]) or np.isnan(gg_noise[ch])):
            snr_fit2[ch] = np.ones_like(spec_vel_array)
        else: 
            snr_fit2[ch] = 1 + gg_alias_func(spec_vel_array, v2[ch], s2[ch], a2[ch], p2[ch])

        snr_spec[ch] = spec[ch,:] / gg_noise[ch] if not np.isnan(gg_noise[ch]) else spec[ch,:] / np.max(spec[ch,:])
    
    """Update spectral figure and fitting """
    # line 1 and line 3 are the gg fitting
    # line 2 and line 4 are the dot and line of the data
    for ch in range(4):
        spcfig = carrier.spectra[ch]
        
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
       
        spcfig.y_range.start = 0
        spcfig.y_range.end = np.max(snr_spec[ch])
        # spcfig.y_range.end = noise1[ch] * max(max((fit[ch, :] + 1)), max((fit2[ch, :] + 1)), max(spcs[ch]/noise1[ch]))
        
    """Update spectral texts """
    for ch in range(4):
        spec = carrier.spectra[ch]
        spec.title.text = 'Ch{0}, {1}:{2}:{3} LT, {4:.2f} km'.format(ch,specsname[11:13],specsname[14:16],specsname[17:19],gg_hts[gg_h_idx] )
        sptext = carrier.textboxes[ch]
        sptext.text = u"V\u2081 = {:.2f} m/s <br> S\u2081 = {:.2f} m/s <br> A\u2081 = {:.2f} <br> p\u2081 = {:.2f} <br> V\u2082 = {:.2f} m/s <br> S\u2082 = {:.2f} m/s <br> A\u2082 = {:.2f} <br> p\u2082 = {:.2f} <br> N = {:.2f}".format(
           v1[ch], s1[ch], a1[ch], p1[ch], v2[ch], s2[ch], a2[ch], p2[ch], np.nan if np.isnan(gg_noise[ch]) else 1) # gg_noise[ch] is not used, the plot is essentially SNR so noise level is always 1
    
        
 