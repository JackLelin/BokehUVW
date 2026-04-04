#!/bin/bash
python3 -m bokeh serve MST3uvw.py --allow-websocket-origin=remote1.ece.illinois.edu --port=40314 --prefix=/JRO
