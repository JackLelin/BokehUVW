from bokeh.layouts import column, row
from bokeh.models import RadioButtonGroup, Button
from bokeh.io import curdoc

import init, spc
from RTI import RTI
from UVW import UVW

def page2():
    init.spectra, init.textboxes = spc.spctraConfig()
    curdoc().clear()

    #Add additional buttons here
    Home = init.Home

    Panels = RadioButtonGroup(labels=["RTI", "UVW"], active=0, width = 400)

    button_layout = row(Home, Panels)
       
    #RTI Layout
    RTI_plot = RTI()
    RTI_layout = column([RTI_plot, init.RTI_color_menu])
    
    #UVW Layout
    UVW_plot = UVW()
    UVW_layout = column([UVW_plot, init.UVW_color_menu])
    
    #Clear current document and add page2 w/RTI Tab
    
    # Spectra_layout = column([row([init.spectra[i], init.textboxes[i]]) for i in range(4)])
    Spectra_layout = row(column(init.spectra),column(init.textboxes))
    Plotting_layout = row([RTI_layout, Spectra_layout])

    page2_doc = curdoc()
    page2_doc.add_root(button_layout)
    page2_doc.add_root(Plotting_layout)
    
    def button_cb(attr, new, old):
        
        if(Panels.active == 1): #This if block loads UVW layout and removes RTI
            Plotting_layout.children[0] = UVW_layout
        
        elif(Panels.active == 0): #This elif block loads RTI and removes UVW
            Plotting_layout.children[0] = RTI_plot
    
    def plot_callback(attr, new, old):
        
        #Reload both tabs based on a change in slider or colorbar value
        RTI_layout.children[0] = column(RTI())
        UVW_layout.children[0] = column(UVW())
    
    #Callbacks to changes in color menu or slider
    
    init.RTI_color_menu.on_change('value', plot_callback)
    init.UVW_color_menu.on_change('value', plot_callback)
    
    Panels.on_change('active', button_cb)

        
