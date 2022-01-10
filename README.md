# BokehUVW

## Start the bokeh server

In ternimal at the bokeh project directory type  
`pythonn3 -m bokeh serve [name of folder] --allow-websocket-origin=remote1.ece.illinois.edu --port=[port number] --prefix=[prefix]`

The website will be `https://remote1.ece.illinois.edu/[prefix]/[name of folder]`

## Config apache

In `/etc/apache2/sites-available` make a config file `*.conf` (or in a existing *.conf ), then add  

    <Location /[prefix]/[name of folder]>
        ProxyPass         http://localhost:[port number]/[prefix]/[name of folder]
        ProxyPassReverse  http://localhost:[port number]/[prefix]/[name of folder]
    </Location>

    <Location /[prefix]/[name of folder]/ws>
        ProxyPass         ws://localhost:[port number]/[prefix]/[name of folder]/ws
        ProxyPassReverse  ws://localhost:[port number]/[prefix]/[name of folder]/ws
    </Location>

    Alias /[prefix]/static /usr/local/lib/python3.8/dist-packages/bokeh/server/static
    <Directory /usr/local/lib/python3.8/dist-packages/bokeh/server/static>
        Options +Indexes
        Require all granted
    </Directory>

## config `init.py`

Change the `thumbnail_url` to 
`thumbnail_url = "[prefix]/static/thumbnail_img/y{}/{}"`


# Folders

## `origin/`

Abdullah's version is in this directory

## `static/`

thumbnail images are in this directory
