---
layout: page
title: Projects
permalink: /projects/
---

#### Source code - [GitHub repos (@idcrook)](https://github.com/idcrook?tab=repositories){: target="_blank"}

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->

- [Projects](#projects)
    - [Servers / Services](#servers--services)
    - [3D Printering](#3d-printering)
        - [3D Print designs](#3d-print-designs)
        - [Software](#software)
        - [3D Printers](#3d-printers)
        - [**Atlas 3D scanner**](#atlas-3d-scanner)
    - [Raspberry Pi](#raspberry-pi)
- [Archives](#archives)
    - [Demos / Presentations](#demos--presentations)
        - [Raspberry Pi Demos](#raspberry-pi-demos)
            - [RGB LED web control demo (2016)](#rgb-led-web-control-demo-2016)
            - [IoT with MQTT and Javascript (2017)](#iot-with-mqtt-and-javascript-2017)
    - [Courses](#courses)

<!-- markdown-toc end -->


Servers / Services
------------------

I use a [homespun ***Kubernetes***](https://github.com/idcrook/kubernetes-homespun){: target="_blank"} cluster for some services from my home network.

| Role                | Service                                                      | Address                                                                               |
|---------------------|--------------------------------------------------------------|---------------------------------------------------------------------------------------|
| Static webserver    | [lighttpd](http://www.lighttpd.net){: target="_blank" }      | [https://www.crookster.org](https://www.crookster.org/){: target="_blank" }           |
| IoT Data Logging    | [phant](http://github.com/idcrook/phant){: target="_blank" } | [https://data.crookster.org](https://data.crookster.org/){: target="_blank" }         |
| RSS Feed Aggregator | [Miniflux](https://miniflux.app/){: target="_blank" }        | [https://miniflux.crookster.org](https://miniflux.crookster.org/){: target="_blank" } |

3D Printering
-------------

### 3D Print designs

Github repo: [idcrook/psychic-winner: Designs for 3D printering (objects, source files)](https://github.com/idcrook/psychic-winner){: target="_blank"}
-	for example: [Bicycle and Car iPhone 6 Plus Mount family](https://github.com/idcrook/psychic-winner/blob/main/iphone_6plus_mount_family/#readme){: target="_blank" }

More designs on [thingiverse account](http://www.thingiverse.com/dpc/designs){: target="_blank"}

### Software

- [OctoPrint](http://octoprint.org)
- [Cura LulzBot Edition - LulzBot](https://www.lulzbot.com/cura)
- [Simplify3D Software - All-In-One 3D Printing Software](https://www.simplify3d.com/)
- [MakerBot Desktop (Software)](https://support.makerbot.com/learn/makerbot-desktop-software/release-notes/makerbot-desktop-release-notes_13520)


### 3D Printers


- [LulzBot Mini](https://www.lulzbot.com/store/printers/lulzbot-mini)
  -	Timelapse with an attached [camera](https://www.youtube.com/watch?v=2JExahTK4Vo&feature=youtu.be)
- [The MakerBot Replicator 2X 3D Printer](https://www.makerbot.com/makerbot-replicator-2x/)
- [Monoprice MP Mini Delta 3D Printer](https://www.monoprice.com/product?p_id=21666)
- [Monoprice MP Maker Pro Mk.1, Auto Level, Touch screen, 300x300x400mm (Open Box)](https://www.monoprice.com/product?c_id=306&cp_id=30601&cs_id=3060101&p_id=35525&seq=1&format=2)

### **Atlas 3D scanner**

-	I built one! - [blog post](/Atlas3D-scanner-ftw/)
-	[Kickstarter project](https://www.kickstarter.com/projects/1545315380/atlas-3d-the-3d-scanner-you-print-and-build-yourse){: target="_blank"} behind it

Raspberry Pi
------------

-	**Raspberry Pi Time and Temperature Display** ![timetemp photo >](/images/updated-timetemp-June-2018.jpeg){: width="120px" }
	-	Logs measurements using "IoT Data Logging" service
	-	[Live Charts](https://github.crookster.org/timetemp/){: target="_blank"}
	-	Recent [blog post](/Moving-Indoor-Weather-Logging-To-Phant/), code [on Github](https://github.com/idcrook/timetemp){: target="_blank"}

Archives
========

Demos / Presentations
---------------------

### Raspberry Pi Demos



#### RGB LED web control demo (2016)

In a hands-on demo, everyone gets to wire up and control a multi-color LED using a real-live Raspberry Pi.

- 	RGB LED web control demo \[[Slides](http://idcrook.github.io/rpi-hw-js-demo/)\] with [rgb-slider](https://github.com/idcrook/rgb-slider) simple jquery controls.

	-	[First presented](/Raspberry-Pi-and-JavaScript-Jam/) at a [local Meetup](http://www.meetup.com/NoCo-JavaScript-Meetup/events/224542835/).
	-	Also at: [a Full-Stack class](/More-RasPi-Javascript/) and [Fort Collins Girls Who Code](/Even-More-RasPi-Javascript/) meeting
	-	Full [code repo](https://github.com/idcrook/rpi-hw-js-demo), including demo [pt. 1](https://github.com/idcrook/rpi-hw-js-demo/blob/gh-pages/demo_notes/demo1.md) / [pt. 2](https://github.com/idcrook/rpi-hw-js-demo/blob/gh-pages/demo_notes/demo2.md)

#### IoT with MQTT and Javascript (2017)

Using networked sensors, real-time monitoring and updates.

- [IoT with MQTT and Javascript](https://github.com/idcrook/rpi-iot-demo-2017), Another hands-on Raspberry Pi demo
  - \[[Slides](http://idcrook.github.io/rpi-iot-demo-2017/presentation.html)\]


Courses
-------

#### Foundations of Data Science Workshop

<dl>
  <dt>Springboard.com, Fall 2015</dt>
  <dd>
    <a href="https://github.com/idcrook/SR_Foundations_DS_Fall_2015" target="_blank">Github repo</a> - Capstone <a href="https://github.com/idcrook/SR_Foundations_DS_Fall_2015/tree/master/capstone" target="_blank">project and presentation</a>
  </dd>
</dl>
