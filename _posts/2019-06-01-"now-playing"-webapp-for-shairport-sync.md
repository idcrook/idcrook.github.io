---
layout: post
title: New "Now Playing" Webapp for shairport-sync
date: 2019-06-01
mathjax: False
comments: False
image: /images/{imagepath}
---

The [Version 3.3 release]() of \[`shairport-sync`]() released last weekend includes MQTT metadata support. It enabled me to create a very useful webapp in the last week (gotta love MQTT!). The focused webapp displays the currently playing song in iTunes (using Airplay) and allows some basic playback controls to be performed. It is fact and simple and already have improved my Apple Music experience at home.

Ingredients of the recipe
-------------------------

Installing and Configuring the webserver app
--------------------------------------------

Technology in the app
---------------------

### basic overview

-	**webserver**:
	-	subscribes to MQTT topics related to the player metadata
	-	relays remote control commands by publishing to an MQTT `remote` interface (that `shairport-sync` subscribes to)
-	**client**:
	-	display the metadata sent by the webserver
	-	provide controls UI that sends remote control requests to webserver

#### Python 3 in the server

For MQTT support, the [paho-mqtt](https://www.eclipse.org/paho/clients/python/) python library is used.

The webserver and socket.io are done using [Flask](http://flask.pocoo.org) and [flask-socketio](https://flask-socketio.readthedocs.io/en/latest/), respectively. The HTML files in `templates` use Flask's baked-in support for **jinja2**.

#### ECMAScript in the client

[jQuery](https://code.jquery.com/jquery/)  handles updating the UI and responding to controls events. The webpage also uses [Bootstrap 3](https://getbootstrap.com/docs/3.3/) elements (and styling).

The [socket.io Javascript Client](https://github.com/socketio/socket.io-client) handles the events and message passing between the server and client.
