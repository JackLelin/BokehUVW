from bokeh.layouts import column, row
from bokeh.models import RadioButtonGroup, CheckboxButtonGroup, CustomJS, Select, RangeSlider
from bokeh.io import curdoc

import init,spc, RTI, UVW

def page2(event):

    init.sps, init.textboxes = spc.spcs('')

    figname = curdoc().get_model_by_id(model_id=event._model_id) #extract user selection

    print(figname.title.text)

    init.date = figname.title.text[5:15]
    init.yyyy = init.date[0:4]
    init.mm = init.date[5:7]
    init.dd = init.date[8:10]
    
    curdoc().clear()

    #Add additional buttons here
    Home = CheckboxButtonGroup(labels=['Home'], active=[], width = 200)
    Home.js_on_click(CustomJS(args=dict(urls=['https://remote1.ece.illinois.edu/JRO/ValleyExp']),code="""window.open(urls, "_self");"""))
    Panels = RadioButtonGroup(labels=["RTI", "UVW"], active=0, width = 400)

    button_layout = row(Home, Panels)
    
    #RTI Layout
    RTI_color_menu = Select(options = init.colors, value = init.RTI_color_menu_value, title = 'Color', width = 500)
    RTI_slider = RangeSlider(start=init.rti_low, end=init.rti_high, value=init.RTI_slider_value, step=.1, title="dB Range", width = 300)
    RTI_plot = RTI.RTI()
    RTI_page = column([RTI_plot, RTI_slider, RTI_color_menu])
    
    #UVW Layout
    UVW_color_menu = Select(options = init.colors, value = init.UVW_color_menu_value, title = 'Color', width = 500)
    U_slider = RangeSlider(start=init.u_low, end=init.u_high, value=init.U_slider_value, step=.1, title="Eastern Wind Range (m/s)", width = 300)
    V_slider = RangeSlider(start=init.v_low, end=init.v_high, value=init.V_slider_value, step=.1, title="Northern Wind Range (m/s)", width = 300)
    W_slider = RangeSlider(start=init.w_low, end=init.w_high, value=init.W_slider_value, step=.1, title="Upward Wind Range (m/s)", width = 300)
    UVW_plot = UVW.UVW()
    UVW_page = column([UVW_plot, column([init.U_slider, init.V_slider, init.W_slider]), UVW_color_menu])
    
    page2_layout = column(button_layout,RTI_page)

    #Clear current document and add page2 w/RTI Tab
    page2_doc = curdoc()
    page2_doc.add_root(page2_layout)
    
    def button_cb(attr, new, old):
        if(Panels.active == 1): #This if block loads UVW layout and removes RTI
            page2_layout.children[-1] = UVW_page
        
        elif(Panels.active == 0): #This elif block loads RTI and removes UVW
            page2_layout.children[-1] = RTI_page

    Panels.on_change('active', button_cb)    

    def plot_callback(attr, new, old):
        init.UVW_color_menu_value = UVW_color_menu.value
        init.RTI_color_menu_value = RTI_color_menu.value
        
        init.RTI_slider_value = RTI_slider.value
        init.U_slider_value = U_slider.value
        init.V_slider_value = V_slider.value
        init.W_slider_value = W_slider.value
        #Reload both tabs based on a change in slider or colorbar value
        RTI_page = column([RTI(), RTI_color_menu])
        UVW_page = column([UVW(), UVW_color_menu])
    
    #Callbacks to changes in color menu or slider
    
    RTI_color_menu.on_change('value', plot_callback)
    UVW_color_menu.on_change('value', plot_callback)
    
    RTI_slider.on_change('value_throttled', plot_callback)
    U_slider.on_change('value_throttled', plot_callback)
    V_slider.on_change('value_throttled', plot_callback)
    W_slider.on_change('value_throttled', plot_callback)
    

        
