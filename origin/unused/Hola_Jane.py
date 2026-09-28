from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select, Div, CheckboxButtonGroup, RadioButtonGroup, CustomJS
from bokeh.models.widgets import Tabs, Panel
from bokeh.plotting import figure, output_file, show
from numpy.random import random, normal, lognormal
from numpy import roll,array


"""
fig1 = figure()
fig1.circle([0,1,2],[1,3,2])
fig2 = figure()
fig2.circle([0,0,2],[4,-1,1])
l1 = layout([[fig1, fig2]], sizing_mode='fixed')
l2 = layout([[fig2]],sizing_mode='fixed')
tab1 = Panel(child=l1,title="This is Tab 1")
tab2 = Panel(child=l2,title="This is Tab 2")
tabs = Tabs(tabs=[ tab1, tab2 ],active=tab_active)
tabs.on_change('active', panelActive)
curdoc().add_root(tabs)
"""

"""
tabs = Tabs(tabs=[tab_01,tab_02])
def tabs_on_change(attr, old, new):
   print("the active panel is " + str(tabs.active))
   plot_tab_function(tabs.active) #<--your plotting code here
tabs.on_change('active', tabs_on_change)

Here, tabs.active is the index of the selected tab.
"""

"""
import io

output = io.StringIO()
output.write('First line.\n')
print('Second line.', file=output)

# Retrieve file contents -- this will be
# 'First line.\nSecond line.\n'
contents = output.getvalue()

# Close object and discard memory buffer --
# .getvalue() will now raise an exception.
output.close()
"""

def color_menu_on_change(attr, old, new): 
    
    def quark_cb(handler):
        quark=quarks[handler]
        page2(quark)

    quark_button_group.on_click(quark_cb)
        
def page2(input1):
                                
    def page_reload(attr, old, new):
                           
        curdoc().clear()
        layout2 = column()
        layout3 = column()                      
        pan1 = Panel(child=layout1,title="Entry")
        pan2 = Panel(child=layout2,title="UVW")
        pan3 = Panel(child=layout3,title="RTI")    
        panels=[pan3,pan2,pan1]     
                      
        nonlocal tnow
        #global tnow
        
        print(attr,old,new,tab_state.now,tnow,tab_state)    
        if type(new) == int:    
            tab_state.now=new
            tnow=new
            
        tabs = Tabs(tabs=panels,active=tnow)
        curdoc().add_root(tabs)
        tabs.on_change('active', page_reload)    

        div = Div(text = input1+': '+word_menu.value + ' ' + names_menu.value, style={'font-size': '100%', 'color': color_menu.value})
        btts = row(word_menu, names_menu)
        txts = row(div)
        layout2.children += [btts, txts]   
        layout3.children += [txts, btts]
       
    words = ['hello', 'hi', 'hola']
    word_menu = Select(options = words, value = words[0], title = 'words')
    word_menu.on_change('value', page_reload)
    
    names = ['John', 'Jim', 'Jane']
    names_menu = Select(options = names, value = names[0], title = 'names')
    names_menu.on_change('value', page_reload)  
    
    class mem(object): # create a blank class named mem to create objects to store and share data between function calls 
        pass
    tab_state=mem() # instantiate mem to share tab_state data
    tab_state.name = 'image tabs'
    tab_state.now = None # since no tab exists so far ... but that will change 
    
    tnow=0
    page_reload('dum','dum',tnow)  

# page 1 is constructed starting here    

layout1 = column()
curdoc().add_root(layout1)

div = Div(text = 'hello, select a color from below')

colors = ['--', 'blue', 'red', 'green']
color_menu = Select(options = colors, value = colors[0], title = 'Color')
layout1.children += [column(div, color_menu)]
color_menu.on_change('value', color_menu_on_change)

quarks = ['up', 'down', 'charm', 'current', 'top', 'bottom'] 
quark_button_group = RadioButtonGroup(labels=quarks, active=0)
layout1.children +=[quark_button_group] 

#tnow = 0