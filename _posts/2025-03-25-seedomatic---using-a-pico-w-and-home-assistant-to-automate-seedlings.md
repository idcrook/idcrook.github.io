---
layout: post
title: Seedomatic - Using Home Assistant to Automate Seedlings
date: 2025-03-25
mathjax: False
comments: False
image: /images/three_bed_temps.png
---

I have a vegetable garden and start seedlings indoors during the winter. I recently renovated my automation setup for this to be based in Home Assistant.


## What Do I Need Automation For?

It comes down to temperature control. Seeds germinate best under certain conditions (moisture, temperature, etc.) with the main thing I needed to do was soil temperature control.

I have seedling tray-sized heat mats. There is no temperature monitoring included on these- just power or no power. This was a simple enough problem to solve:

1. Measure temperature
1. If temperature is above target temperature, turn heat pad **OFF**.
1. If temperature is below target temperature, turn heat pad **ON**.
1. Repeat cycle

### Previous solution: MQTT, Wemo smart outlets and Python script

I have a few Wemo smart outlets. There is a python library for monitoring and controlling these over the network. So the **ON**/**OFF** aspect of the heat pads can be done using these.

MQTT is a reliable PubSub solution. Useful in home automation, it runs great within a  home LAN. My MQTT broker is `mosquitto` running on a Raspberry Pi. You can publish sensor data to MQTT from wireless nodes like ESP32 or Pico W micro-controllers. This sensor data can be consumed by other processes.

Since it was in python, it was simple enough to switch to a different platform (Wemo to Kasa) since there are existing python libraries available. This was running as a systemd service on a Raspberry Pi.

- [indoor-seedomation - python temperature monitor and heater control ](https://github.com/idcrook/indoor-seedomation?tab=readme-ov-file#indoor-seedomation)

I have a Raspberry Pi Pico W ("W" is for Wi-Fi, I guess) microcontroller for the sensor part. Add MicroPython and DS18B20 waterproof temperature sensor that can be embedded directly in the seedling trays and soil, and now the temperature sensing is handled.

- [MQTT sensor node on Pico W](https://github.com/idcrook/picow-projects/tree/main/multi_monitor)


## Updated Solution: Home Assistant MQTT Discovery for Sensors

Over the winter I set up a Raspberry Pi running Home Assistant OS. I migrated my collection of zigbee devices and basically everything else away from smartthings and Homebridge.  Home Assistant ecosystem has an incredible number of well-supported integrations! What if I could use some native features of Home Assistant to take over the temperature control task for my seedlings?

I just love the productivity available with micropython. Can interate quickly, even running a REPL on target device for debug exploration. I started from my previous Pico W MQTT sensor node, and investigated something in Hass called [MQTT (Auto) Discovery](https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery). Turns out once a few important concepts are understood, it's relatively simple to turn any sensor into one recognized by Hass. It's mainly just JSON messages published into an agreed-upon MQTT hierarchy, and then it "Just Works".

[Yet Another Home Assistant Temperature monitor, using micropython and Pico W](https://github.com/idcrook/yaha_temperature_monitor)

### Microcontroller Wi-Fi Issues?

In a "word": [*Hardware Watchdog Timer*](https://github.com/idcrook/yaha_temperature_monitor/blob/7fda99e39fb2ca673fdd78e5ac31396a759f5933/main.py#L351-L358)

One area I greatly improved of for this second generation was more robust wireless networking. Making use of the Hardware Watchdog Timer available in micropython and on the Pico W, I was able to have my sensor nodes stay up even across rebooting routers or flaky network signaling.

Whereas previously, I would have to go unplug and re-plug in the Pico W whenever I rebooted a router or it lost its network connection, now it resets itself, and can consistently re-connect to wireless network without physical intervention.

### Home Assistant Has A Built-in "Generic Thermostat"

Home Assistant Has A Built-in "Generic Thermostat" Device. Just connect a temperature (sensor) and in my case a smart power strip outlet (control), and set your desired temperature range and it will take care of monitoring and control.

![Heat Mat Bed 2 soil Temperature <>](/images/bed_heat_mat_temp.png "Heat Mat Bed 2 soil Temperature" )
![Heat Mat on off control <>](/images/bed_heater_control.png "Heat Mat on off control" )

Since these are now Hass native controls and devices, they can be arranged like any other dashboard.


![Bed temperatures, ambients, thermostats, and smart strip <>](/images/three_bed_temps.png "Bed temperatures, ambients, thermostats, and smart strip")

## Conclusion

I have moved almost my entire "smart home" over to Home Assistant, and now that I am familiar with some of its internals, I suspect even more will be added to my home's configuration over time.
