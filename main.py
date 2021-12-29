from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import  Select, Div
from bokeh.plotting import figure
from glob import glob1
import init

from bokeh.events import Tap, MouseEnter, MouseLeave
from page2 import page2

def year_select_handler(attr, old, new):
    doc.remove_root(thumbnail_layouts[old])
    doc.add_root(thumbnail_layouts[new])
    

def year_images(year): #Generating Function of thumbnails
    #doc.remove_root(init.inital_maps)
    imgs = sorted(glob1("static/thumbnail_img/y"+year+"/", '*')) 
    """Plot images of the given year"""
    #init.RTI_layout = column()
    plots = []
    for i in range(0, len(imgs)//3):
        tmaps = []
        for v in range(3):
            tmap = figure(plot_width=350, plot_height=160,
                          title=imgs[3*i+v],
                          x_range=(0, 350), y_range=(0, 160),
                          active_drag=None,
                          toolbar_location=None)
            tmap.image_url(url=["ValleyExp_dev/static/thumbnail_img/y"+year+"/"+imgs[3*i+v]], x=[0], y=[160],
                            w=[350], h=[160])
            tmap.grid.visible= False
            tmap.axis.visible= False
            tmap.outline_line_color = None
            tmap.title.text_font_size = '10pt'
            tmap.on_event(MouseEnter, thumbnail_effect1_handler)
            tmap.on_event(MouseLeave, thumbnail_effect2_handler)
            tmap.on_event(Tap, thumbnail_click_handler)      
            tmaps += [tmap]
        plots.append(row(tmaps))
    
    return column(plots) 

def thumbnail_effect1_handler(event): #Function that highlights black around thumbnail when mouse hovers
    fig = curdoc().get_model_by_id(model_id=event._model_id)
    if fig is not None:
        print(event._model_id)
        fig.outline_line_color = 'black'
    
def thumbnail_effect2_handler(event): #Function that takes away that black outline when mouse leaves thumbnail
    fig = curdoc().get_model_by_id(model_id=event._model_id)
    if fig is not None:
        fig.outline_line_color = None

def thumbnail_click_handler(event):
    figname = curdoc().get_model_by_id(model_id=event._model_id) #extract user selection
    print(figname.title.text)

    init.date = figname.title.text[5:15]
    init.yyyy = init.date[0:4]
    init.mm = init.date[5:7]
    init.dd = init.date[8:10]

    page2()

doc = curdoc()#initializing the document

entry_layout = column()

Title_txt = Div(text = 'Valley experiment at JRO', style={'font-size': '200%', 'color': 'black'}, width =1200)
Info_txt = Div(text = "This page contains a summary of the winds data measured at JRO during MST-ISR campaigns. To explore the data in an interactive mode click on the winds of the day of interest. By default the results shown are from the last analyzed year. Previous years can be selected using the drop-down list.")
Secondary_txt = Div(text = "Click on a thumbnail image and then head click on a tab, to view the map", style={'font-size': '120%', 'color': 'black'}, width =1200)
entry_layout.children += [column(Title_txt, Info_txt)]

dname = init.dname
years = sorted(glob1(dname, "*"))
year_menu = [(year, year) for year in years]
default_year = init.yyyy

year_select = Select(title='Select a year:', value=default_year, options=year_menu)
year_select.on_change('value',year_select_handler)
entry_layout.children += [year_select]

doc.add_root(entry_layout)
doc.add_root(Secondary_txt)

thumbnail_layouts = {year:year_images(year) for year in years}
doc.add_root(thumbnail_layouts[default_year])

doc.title = "JRO Valley experiments"








