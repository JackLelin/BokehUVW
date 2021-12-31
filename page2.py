from bokeh.layouts import column, row
from bokeh.models import RadioButtonGroup

import init, spc
from RTI import RTI_plotting
from UVW import UVW_plotting

def Page2(carrier):

    # Initialize the buttons
    Panels = RadioButtonGroup(labels=["RTI", "UVW"], active=0, width = 400)
    Button_layout = row(carrier.Home, Panels)
    
    # The carrier loads all data
    carrier.loadData()
    carrier.spectra, carrier.textboxes = spc.spctraConfig()

    #RTI Layout
    RTI_plot = RTI_plotting(carrier)
    RTI_layout = column([RTI_plot, carrier.RTI_color_menu])
    
    #UVW Layout
    UVW_plot = UVW_plotting(carrier)
    UVW_layout = column([UVW_plot, carrier.UVW_color_menu])
        
    # Spectra_layout = column([row([init.spectra[i], init.textboxes[i]]) for i in range(4)])
    Spectra_layout = row(column(carrier.spectra),column(carrier.textboxes))
    Plotting_layout = row([RTI_layout, Spectra_layout])
   
    def button_cb(attr, new, old):
        # Clear current document and add page2 w/RTI Tab
        if(Panels.active == 1): #This if block loads UVW layout and removes RTI
            Plotting_layout.children[0] = UVW_layout
        
        elif(Panels.active == 0): #This elif block loads RTI and removes UVW
            Plotting_layout.children[0] = RTI_layout
    
    def plot_callback(attr, new, old):
        #Reload both tabs based on a change in colorbar value
        RTI_layout.children[0] = RTI_plotting(carrier)
        UVW_layout.children[0] = UVW_plotting(carrier)
    
    #Callbacks to changes in color menu or slider
    carrier.RTI_color_menu.on_change('value', plot_callback)
    carrier.UVW_color_menu.on_change('value', plot_callback)
    
    Panels.on_change('active', button_cb)

    return column([Button_layout, Plotting_layout]) 
        
"""
+----------------------------------------------------page2-----column()----------------------------------------------------------------+
|                                                                                                                                      |
|     +------------------------------------------------Button_layout----row()----------------------------------------------------+     |
|     |      |*******HOME*******|        |*****RTI*****|*****UVW*****|                                                           |     |
|     +--------------------------------------------------------------------------------------------------------------------------+     |
|                                                                                                                                      |
|     +-----------------------------------------------Plotting_layout------row()-------------------------------------------------+     |
|     |                                                                                                                          |     |
|     |   +-------------RTI_Layout/UVW_Layout---column()---+         +------------------------Spectra_layout---row()----------+  |     |
|     |   |                                                |         |  +------column()-------+      +-------column()------+  |  |     |
|     |   |                                                |         |  |  *****Figure()****  |      |  ******Div()******  |  |  |     |
|     |   |     +------return from--RTI()/UVW()-----+      |         |  |  *     Spec0     *  |      |  *     Text0     *  |  |  |     |
|     |   |     |                                   |      |         |  |  *****************  |      |  *****************  |  |  |     |
|     |   |     |                                   |      |         |  |                     |      |                     |  |  |     |
|     |   |     |                                   |      |         |  |  *****Figure()****  |      |  ******Div()******  |  |  |     |
|     |   |     |                                   |      |         |  |  *     Spec1     *  |      |  *     Text1     *  |  |  |     |
|     |   |     |                                   |      |         |  |  *****************  |      |  *****************  |  |  |     |
|     |   |     |                                   |      |         |  |                     |      |                     |  |  |     |
|     |   |     |                                   |      |         |  |  *****Figure()****  |      |  ******Div()******  |  |  |     |
|     |   |     +-----------------------------------+      |         |  |  *     Spec2     *  |      |  *     Text2     *  |  |  |     |
|     |   |                                                |         |  |  *****************  |      |  *****************  |  |  |     |
|     |   |                                                |         |  |                     |      |                     |  |  |     |
|     |   |      ***RTI_color_menu/UVW_color_menu***       |         |  |  *****Figure()****  |      |  ******Div()******  |  |  |     |
|     |   |      ************Select()***************       |         |  |  *     Spec3     *  |      |  *     Text3     *  |  |  |     |
|     |   |      ***********************************       |         |  |  *****************  |      |  *****************  |  |  |     |
|     |   |                                                |         |  +---------------------+      +---------------------+  |  |     |
|     |   +------------------------------------------------+         +--------------------------------------------------------+  |     |
|     |                                                                                                                          |     |
|     +--------------------------------------------------------------------------------------------------------------------------+     |
|                                                                                                                                      |
+--------------------------------------------------------------------------------------------------------------------------------------+
"""