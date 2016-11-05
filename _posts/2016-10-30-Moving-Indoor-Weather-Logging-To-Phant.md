---
layout: post
title: Porting indoor weather (BMP085) logging project to SFE Phant
---

For a while now, have had a time/temp logging system in my house.  It is still hosted on my very first Raspberry Pi, and uses a BMP085 temperature/pressure sensor, and two 1.2" LED displays from Adafruit. The logging on <s>Pachube</s> -> <s>COSM</s> -> *Xively* needed to be updated to something else, so I decided to use [Phant](http://phant.io) from Sparkun Electronics (SFE).


# Existing setup

 - 2 of [Adafruit 1.2" 4-Digit 7-Segment Display w/I2C Backpack](https://www.adafruit.com/product/1268)
 - [BMP085 sensor breakout board](https://www.adafruit.com/product/391)
 - Raspberry Pi Model B (1st gen.) plus PSU and Ethernet networking, running Raspbian
 - [I2C Level converter](https://www.adafruit.com/product/757)
 - Solderless Breadboard, wires, and [Pi Cobbler Breakout + Cable for Raspberry Pi](https://www.adafruit.com/products/914)
 
There are two LED displays: one for the time, and one for the temperature. The displays are programmed through I2C, and the BMP085 sensor is also located on the shared I2C bus.

![Display of the time and temperature](/images/time_temp_update.jpg)

The green square hollow prism with a pattern of holes in its top center is the BMP085 sensor, in a 3D-printed case.  And the LED displays are residing in a bespoke case that was designed and printed by **me** -- one of my earliest forays into 3D Printing.

# Updates

The ["old" version](https://github.com/idcrook/timetemp) (circa Spring 2013) that uploaded to xively.com used old Adafruit python libraries and a EEML XML-based data format. 

This update moved to the new Adafruit python library versions ([LED Backpack](https://github.com/adafruit/Adafruit_Python_LED_Backpack), [BMP](https://github.com/adafruit/Adafruit_Python_BMP)) and used SFE Phant service for data logging (using [python-phant](https://github.com/matze/python-phant)).

## Clock code

The **time** python code was a straight port. Method names changed slightly, and the LED API had been updated to be more user friendly. It was a quick port, as I was able to leverage the example code script.

 - [my_7segment_clock.py](https://github.com/idcrook/Adafruit_Python_LED_Backpack/blob/master/examples/my_7segment_clock.py)

## BMP085 and Data logging

The **temp** port was a little more involved. The BMP sensor python API was basically unchanged, but the logging code needed to be moved to a different scheme. The Phant service (at [https://data.sparkfun.com](https://data.sparkfun.com)) is simple to use. You can generate a new data stream without a login. And logging to/querying from the service uses simple HTTP requests. 

A new stream was created using the web form.  After storing the keys along with downloading a JSON file that contained the key settings, the code was updated. 

 - [logging_sparkfun.py](https://github.com/idcrook/Adafruit_Python_BMP/blob/master/examples/logging_sparkfun.py)

The beauty of open-source python libraries is that you can see the implementation and even fix any bugs you find in the source itself! I found an issue related to reading in the Phant stream settings from aforementioned JSON file, and was able to update the library source code to workaround it.

## Pointers to customized source code

 - [https://github.com/idcrook/Adafruit_Python_LED_Backpack](https://github.com/idcrook/Adafruit_Python_LED_Backpack)
 - [https://github.com/idcrook/Adafruit_Python_BMP](https://github.com/idcrook/Adafruit_Python_BMP)
 - [https://github.com/idcrook/python-phant](https://github.com/idcrook/python-phant)
   - Found some issues w.r.t. loading from JSON config file, so generated a [PR](https://github.com/matze/python-phant/pull/20)
