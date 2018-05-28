---
layout: post
title: Extending HomeKit with Homebridge and Raspberry Pi to All the Things
---

What to do with a Nest thermostat, Belkin WeMo smart switches and lights, web services, and custom home-grown sensors in an Apple household? Can  HomeKit talk to non-HomeKit devices? An excellent project named [Homebridge](https://github.com/nfarina/homebridge) along with its user-provided plugins has the answers.


<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-generate-toc again -->
**Table of Contents**

- [HomeKit's shortfalls](#homekits-shortfalls)
- [Enter homebridge. Easy as Pi](#enter-homebridge-easy-as-pi)
    - [Install on Raspberry Pi 3](#install-on-raspberry-pi-3)
        - [Actual steps that I used](#actual-steps-that-i-used)
        - [Launching homebridge](#launching-homebridge)
- [Homebridge plugins](#homebridge-plugins)
    - [From my `~/.homebridge/config`](#from-my-homebridgeconfig)
    - [Belkin WeMo plugin](#belkin-wemo-plugin)
        - [auto-detect config.json (platform)](#auto-detect-configjson-platform)
    - [Nest plugin](#nest-plugin)

<!-- markdown-toc end -->

# HomeKit's shortfalls

Apple's HomeKit has many promises on a smart, seamless home environment.  And indeed, if you have a collection of devices that directly support HomeKit, it is like living in a future paradise. Doors that unlock when you approach them, speaking into your watch to turn down the lights or crank up the A/C, or check in on your pet when you are fine dining.

Where it fell down though, is the multitude of devices and products that do not have HomeKit support built-in. Indeed, after years of Belkin WeMo ([WeMo Says No HomeKit](http://www.belkin.com/us/support-article?articleNum=187953)), Nest, other one-off "smart home" monitors and controls, the first things I had in my home that actually integrated natively with Apple HomeKit was Philips Hue. And even there as is typical, they direct you to use their one-off apps to register and control their branded devices.

# Enter homebridge. Easy as Pi

 - [homebridge](https://github.com/nfarina/homebridge): "HomeKit support for the impatient"

A node.js-based bridge for HomeKit devices, homebridge can serve to connect assorted types of devices and services into the HomeKit environment.


## Install on Raspberry Pi 3

For this to work, it is assumed:

- you have a Raspberry Pi 3 running Raspbian OS
  - a Pi 2 also should work
  - it's connected to same network that target smart home devices live on
  - ssh access to Pi
- have `nvm` ([node version manager](https://github.com/creationix/nvm)) activated on a raspberry pi 3

There are many instructions on how to image Raspbian onto an micro-SD card and configure for home network.  I run mine without a monitor or keyboard connected, using only Ethernet-connected SSH to connect to and control it.

[https://github.com/nfarina/homebridge/wiki/Running-HomeBridge-on-a-Raspberry-Pi](https://github.com/nfarina/homebridge/wiki/Running-HomeBridge-on-a-Raspberry-Pi)

### Actual steps that I used

`nvm` is a handy utility, and the following assumes you are using latest stable node.js installed using `nvm`.

These may differ from instructions on the wiki as a result, but I have tested and used these actual commands.

```shell
sudo apt-get install -y libavahi-compat-libdnssd-dev

sudo npm install -g --unsafe-perm homebridge hap-nodejs node-gyp
NODE_BIN_DIR=$(dirname `nvm which default`)
NODE_MODULES_DIRS=$(dirname $NODE_BIN_DIR/../lib/node_modules/.)
cd $NODE_MODULES_DIRS/homebridge/
sudo npm install --unsafe-perm bignum
cd $NODE_MODULES_DIRS/hap-nodejs/node_modules/mdns
sudo node-gyp BUILDTYPE=Release rebuild
sudo which node-gyp BUILDTYPE=Release rebuild
```

Now use "normal" [installation](https://github.com/nfarina/homebridge/blob/master/README.md#installation)  instructions.


### Launching homebridge

There are instructions available on how to auomatically launch the homebridge server when your Pi starts up (e.g. [systemd](https://github.com/nfarina/homebridge/wiki/Running-HomeBridge-on-a-Raspberry-Pi#running-homebridge-on-bootup-systemd)), but I use something different. I use `GNU screen` to be able to reconnect to long-running commands (such as node.js servers like `homebridge` is).

```shell
screen -R
which homebridge
/home/pi/.nvm/versions/node/v7.4.0/bin/homebridge
homebridge=$(which homebridge)
$homebridge
# ... homebridge start-up output here
```

# Homebridge plugins


The power and flexibilty of the `homebridge` bridge comes from the [plethora](https://www.npmjs.com/search?q=plugin+for+homebridge) of [plugins](https://www.npmjs.com/search?q=homebridge-plugin) available.
There are, at this writing "586 packages found for "homebridge-plugin". Not all are of the same quality or as widely applicable as each other, and many have been made redundant, but there is likely a plugin existing for something you wish that HomeKit supported.  And if not, you can use Javascript and node.js and the example plugins to make your own... :)


## From my `~/.homebridge/config`

The  `~/.homebridge/config.json` needs to be edited for your devices. Here's a snippet with most custom values obscured.

```json
  "description": "Used as template for creating your own configuration file.",

  "accessories": [
  ],
  "platforms": [
    {
      "platform": "BelkinWeMo",
      "name": "WeMo Platform",
      "noMotionTimer": 60,
      "ignoredDevices": ["DEADEC18FEED"]
    },
    {
      "platform": "Nest",

      "token": "c.crazylonggKtOkenjkhrhrhrhrhrQREQrq"

    }
  ]
```



## Belkin WeMo plugin

Belkin sez no waze. Internet can haz WeMomeKit.

The plugin I used is `homebridge-platform-wemo`

- [https://github.com/rudders/homebridge-platform-wemo](https://github.com/rudders/homebridge-platform-wemo)

```shell
sudo npm install -g homebridge-platform-wemo
```


### auto-detect config.json (platform)

```json
 "platforms": [
    {
      "platform": "BelkinWeMo",
      "name": "WeMo Platform",
      "noMotionTimer": 60,
      "ignoredDevices": []
    }
```

works perfectly!



## Nest plugin

[https://github.com/KraigM/homebridge-nest](https://github.com/KraigM/homebridge-nest)

There are full install instructions in the project's README, and here is just a summary of the steps.

1. setup Nest developer account
2. `sudo npm install -g git+https://github.com/igbopie/homebridge-nest.git`
3. add credentials to config (to get token) and launch homebridge
4. IMPORTANT: From homebridge gather taken in output; update config with token now, and restart
