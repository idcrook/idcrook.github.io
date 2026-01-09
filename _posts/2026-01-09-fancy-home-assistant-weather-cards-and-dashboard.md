---
layout: post
title: Fancy Home Assistant Weather Cards and Dashboard
date: 2026-01-09
mathjax: False
comments: False
image: /images/hass-weather-dashboard.png
---

I recently got a local outdoor weather station and used it a reason to add more weather data to my Home Assistant setup.

![ Weather dashboard](/images/hass-weather-dashboard.png "Custom Weather Dashboard including live data, forecast and conditions map.")

## EcoWitt WS90 and GW3000

I ordered an EcoWitt "Wittboy" kit during the recent holiday deals. It consists of an outdoor solar-powered weather sensor array, and a networked indoor hub. It is the [US version](https://shop.ecowitt.com/collections/weather-station/products/ecowitt-gw3001-gw3011), which uses 915 MHz telemetry.

I created a 3D printed "adapter" for fixing onto a birdhouse pole, making available on Printables: [Ecowitt WittBoy WS90 Weather Station Sensor Array Birdhouse Pole Stand Adapter](https://www.printables.com/model/1485967-ecowitt-wittboy-ws90-weather-station-sensor-array).

![live data](/images/ecowitt-live.png)

The way these weather stations work is that they periodically transmit sensor readings and then the hub receives these broadcasts and logs the data according to how it has been configured.

## Home Assistant Basics

I use Home Assistant OS on a Raspberry Pi 5. I have been using it since even before the Pi 5 was officially supported, and run it on an NVMe SSD drive. It comes with weather forecast support. There seems to be all manner of weather dashboard integrations, but I came across some now-lost Reddit threads which rolled their own weather dashboard views, and I ended up adopting/adapting this approach.

I've link to a version of my Card and Dashboard views below.

## Hass Integrations

There were numerous integrations used to achieve the deshboard views. They are all available via HACS if they are not already included in the officially included ones.

### Hass Integrations - Data

Data

 - Ecowitt official - local API webhook
 - Ecowitt
 - Pirate Weather

### Hass Integrations - Views

For Charts

 - Apex Charts
 - Lovelace Layout Card
 - Plotly Graph Card

#### Ecowitt weather station

There are two options that both work: the "Official Integration" which is not the same as the listed Ecowitt integration.

- "Official Integration" [Ecowitt/ha-ecowitt-iot: This integration uses the locally available http APIs to obtain data from the supported devices inside the local network.](https://github.com/Ecowitt/ha-ecowitt-iot)
- Listed in Home Assistant directory: [Ecowitt - Home Assistant](https://www.home-assistant.io/integrations/ecowitt/)

The former "Official" Ecowitt integration is a local-only API that will create a webhook with its integration. Part of setting it up means configuring the webhook key / URL in the network hub settings.

![hub config](/images/ecowitt-local-api.png)

The latter one using the built-in cloud data logging from the Ecowitt hub (if you have it enabled). Their cloud service keeps a history of readings. I switched from this to the local-only integration after I installed a micro-SD in my network hub.

They both expose the readings as entities (some slight variations in naming) for the device.

#### Pirate Weather

Pirate Weather is a weather forecast system with an API similar to the no-longer-available Dark Sky one.

- [Home Assistant Integration Documentation - Pirate Weather](https://docs.pirateweather.net/en/latest/ha/)

I use it to include weather forecasts. There are all sorts of weather cards and data sources for forecasting. Plenty of easy experimentation to find something you like.

#### Apex Charts

[RomRider/apexcharts-card: 📈 A Lovelace card to display advanced graphs and charts based on ApexChartsJS for Home Assistant](https://github.com/RomRider/apexcharts-card)

#### Lovelace Layout Card

[thomasloven/lovelace-layout-card: 🔹 Get more control over the placement of lovelace cards.](https://github.com/thomasloven/lovelace-layout-card)

#### Plotly Graph Card

[dbuezas/lovelace-plotly-graph-card: Highly customisable Lovelace card to plot interactive graphs. Brings scrolling, zooming, and much more!](https://github.com/dbuezas/lovelace-plotly-graph-card)

Used in the "Wind Rose" chart.

![wind rose chart](/images/hass-windrose-chart.png)


## Sensor Card

There are other weather card views available, but I used the apex chart view. The view is configured manually using YAML.

{% gist 51f27869a4ba4cd78d5cf2be8babe70e sensor-card.yaml %}

![weather card](/images/hass-weather-card.png)

## Weather Dashboard

The entire dashboard is configured through YAML. I found it easiest to edit the YAML in Visual Studio Code, and then copy and paste the whole file, replacing the entire contents of the configuration

It has been split in two parts: the "root" which basically contains templates and DRY default configs for the charts.

{% gist 51f27869a4ba4cd78d5cf2be8babe70e dashboard-root.yaml %}

Here is the whole dashboard expressed in YAML.

{% gist 51f27869a4ba4cd78d5cf2be8babe70e dashboard-view.yaml %}

![weather dashboard](/images/hass-weather-dashboard.png)
