from bokeh.layouts import column, row
from bokeh.models import RadioButtonGroup, Button
from bokeh.io import curdoc

import init,spc
from RTI import RTI
from UVW import UVW

def page2():
    init.sps, init.textboxes = spc.spcs('')
    curdoc().clear()

    # def BackButtonHandler(event):
    #     page2()

    #Add additional buttons here
    Home = init.Home
    # Back = Button(label='Back', width = 200)
    # Back.on_click(BackButtonHandler)
    Panels = RadioButtonGroup(labels=["RTI", "UVW"], active=0, width = 400)

    button_layout = row(Home, Panels)
    
    #initialize local layouts to reduce chance of doubling
    RTI_layout = column()
    UVW_layout = column()
    
    #RTI Layout
    RTI_page = column(RTI())
    RTI_layout.children[-1:] = [column(button_layout, RTI_page, init.RTI_color_menu)]
    
    #UVW Layout
    UVW_page = column(UVW())
    UVW_layout.children[-1:] = [column(button_layout, UVW_page, init.UVW_color_menu)]
    
    #Clear current document and add page2 w/RTI Tab
    
    page2_doc = curdoc()
    page2_doc.add_root(RTI_layout)
    
    def button_cb(attr, new, old):
        
        if(Panels.active == 1): #This if block loads UVW layout and removes RTI
            UVW_page = column(UVW())
            UVW_layout.children[-1:] = [column(button_layout, UVW_page, init.UVW_color_menu)]
            page2_doc.remove_root(RTI_layout)
            page2_doc.add_root(UVW_layout)
        
        elif(Panels.active == 0): #This elif block loads RTI and removes UVW
            RTI_page = column(RTI())
            RTI_layout.children[-1:] = [column(button_layout, RTI_page, init.RTI_color_menu)]
            page2_doc.remove_root(UVW_layout)
            page2_doc.add_root(RTI_layout)
    
    def plot_callback(attr, new, old):
        
        #Reload both tabs based on a change in slider or colorbar value
        RTI_page = column(RTI())
        RTI_layout.children[-1:] = [column(button_layout, RTI_page, init.RTI_color_menu)]
        
        UVW_page = column(UVW())
        UVW_layout.children[-1:] = [column(button_layout, UVW_page, init.UVW_color_menu)]
    
    #Callbacks to changes in color menu or slider
    
    init.RTI_color_menu.on_change('value', plot_callback)
    init.UVW_color_menu.on_change('value', plot_callback)
    
    init.RTI_slider.on_change('value_throttled', plot_callback)
    # init.RTI_slider.on_event('LODEnd', plot_callback)
    init.RTI_slidersyncable = False

    init.U_slider.on_change('value_throttled', plot_callback)
    init.V_slider.on_change('value_throttled', plot_callback)
    init.W_slider.on_change('value_throttled', plot_callback)
    
    Panels.on_change('active', button_cb)

        
