---
layout: post
title: My New "Now Playing" Webapp for shairport-sync
date: 2019-05-31
mathjax: False
comments: False
image: /images/now_playing_sideways_iphone_frame.png
---

 [Version 3.3](https://github.com/mikebrady/shairport-sync/releases/tag/3.3) of [`shairport-sync`](https://github.com/mikebrady/shairport-sync) released last weekend and includes  metadata support on MQTT. "*So what?*" you may ask? I [created an app] to display the metadata and do simple remote controls. Now, I can control my music all around the house or identify currently playing song at a glance.  It's [open-source].

![demo screencap]

I was able to create a useful webapp in a couple days -- gotta love MQTT! The single-purpose webapp displays the currently playing song (over AirPlay® from iTunes®<sup id="a1">[1](#f1)</sup>) and includes  playback controls.  The app itself is fast and simple and already has improved my Apple Music® experience at home.

Ingredients of the recipe
-------------------------

As outlined in the [app's README](https://github.com/idcrook/shairport-sync-mqtt-display/blob/master/python-flask-socketio-server/README.md) there are four main requirements to run the app:

1. **AirPlay®** such as from iTunes® or the Music app in iOS™
2. **`shairport-sync` (with MQTT support)** as an AirPlay® receiver
3. **MQTT broker**
4. A computer that can run the webserver app (Python 3)

Requirements 2., 3., and 4. can all be on the same computer, for example, a Raspberry Pi®

Also you need something to display the single-task webpage. It can be a computer, smartphone or tablet.

It works great even on seven year old Kindle Fire 7" tablets or seven year old iPads (_3rd gen_) running iOS 9. (**_Hint, hint_**: might have a valuable use for those old devices as simple home audio remotes)

The Webapp
--------------------------------------------

![web app screencap >]

There are full instructions in the [install section](https://github.com/idcrook/shairport-sync-mqtt-display/blob/master/python-flask-socketio-server/README.md#install) of the README, including pre-reqs and dependencies, for installing the webserver. I'll defer to those.

There's an [example config file] in the `yaml` format.

 It will look something like this (to the right) in a browser when default `webui` values are used and it's running (connected to MQTT broker, and `shairport-sync` providing metadata to MQTT)

In fact, it is a cropped screenshot taken in iOS.

![add_to_homescreen] ![on_homescreen]

Running as a "webapp", at least on iOS™ will hide most of the Safari browser "chrome" and appear very clean on the full-screen. That is what the "_Add to Home Screen_" does. And tapping the icon from your Home Screen will quickly launch the app and connect to your server.

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

---

<i id="f1">1</i>: Trademarks are the respective property of their owners.[⤸](#a1)


[created an app]: https://github.com/idcrook/shairport-sync-mqtt-display/tree/master/python-flask-socketio-server

[open-source]: https://github.com/idcrook/shairport-sync-mqtt-display

[example config file]: https://github.com/idcrook/shairport-sync-mqtt-display/blob/master/python-flask-socketio-server/config.example.yaml


[demo screencap]: /images/now_playing_iphone_framed.png "Hero shot in iPhone frame of Now Playing webapp"

[web app screencap >]: /images/now_playing_screencap.png "Webapp screen cap on iOS"


[add_to_homescreen]: /images/now_playing_add_to_homescreen.jpg "Share sheet menu with 'Add to Home Screen'"
[on_homescreen]: /images/now_playing_on_homescreen.jpg "Launch icon on home screen"
