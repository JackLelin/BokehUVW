#!/bin/bash
#python3 -m bokeh serve MST3uvw.py --allow-websocket-origin=remote1.ece.illinois.edu/JRO --port=40314 --prefix=/JRO
#python3 -m bokeh serve MST3uvw.py --port=40314 --prefix=/JRO
/rd0/madrigal/python312/bin/python3 -m bokeh serve ./ --allow-websocket-origin=remote1.ece.illinois.edu --allow-websocket-origin=localhost:40314 --allow-websocket-origin=remote1.ece.illinois.edu:80 --port=40314 --prefix=/JRO
