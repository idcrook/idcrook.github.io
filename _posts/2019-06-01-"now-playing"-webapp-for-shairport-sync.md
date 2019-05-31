---
layout: post
title: New "Now Playing" Webapp for shairport-sync
date: 2019-06-01
mathjax: False
comments: False
image: /images/{imagepath}
---

The [Version 3.3 release]() of [`shairport-sync`]() released last weekend includes MQTT metadata support. It enabled me to create a very useful webapp in the last week (gotta love MQTT!). The focused webapp displays the currently playing song in iTunes (using Airplay) and allows some basic playback controls to be performed. It is fact and simple and already have improved my Apple Music experience at home.

## Ingredients of the recipe


## Installing and Configuring the webserver app



## Technology in the app

### Python 3 in the server


For MQTT support, the paho-mqtt library.
The webserver and socket.io are done using flask and flask-socketio, respectively
The HTML files in `templates` use the baked-in **jinja2** support


### ECMAScript in the client

It uses Bootstrap 3 components and styling, jQuery, and socket.io Javascript Client.
