---
layout: post
comments: true
title: Revisiting Homekit USB Webcam on Raspberry Pi 3
mathjax: false
image: /images/2018-08-25-Favorite-cameras-summary-card.jpg
---

On home _HomeKit_ setup, some `homebridge` plugins (Nest, WeMo) needed updating. And flaky webcam performance needed addressing. It was also time to update the `node.js` install. Got it all completed.

Previously:

 - [HomeKit connecting to Nest thermostat and Belkin WeMo devices](/Extending-HomeKit-with-Homebridge-and-Raspberry-Pi/ "Extending HomeKit with Homebridge and Raspberry Pi to All the Things")
 - [Adding a Webcam to Homekit Using a Raspberry Pi 3](/Adding-A-Webcam-To-HomeKit/ "Getting a USB Webcam to work with Homebridge")


## `node.js` and `homebridge`+`plugins` re-install

Before troubleshooting the camera, update all the things. As [`nvm`](https://github.com/creationix/nvm) was already installed, used it to update `node` + `npm`.

```bash
nvm install node

# upgrade to latest npm on current node version
nvm install-latest-npm

nvm alias default node

# system-wide node links
file `nvm which node`
NODE_BIN_DIR=$(dirname `nvm which node`)
sudo ln -sf ${NODE_BIN_DIR}/node /usr/local/bin/node
sudo ln -sf ${NODE_BIN_DIR}/npm /usr/local/bin/npm

# Now install the homebridge modules
sudo apt-get install -y libavahi-compat-libdnssd-dev
sudo npm install -g --unsafe-perm homebridge

# plugins
sudo npm install -g homebridge-platform-wemo
sudo npm install -g homebridge-nest
sudo npm install -g homebridge-camera-ffmpeg

# system-wide link that systemd service uses
sudo ln -sf $(which homebridge) /usr/local/bin/homebridge
```

## Webcam improvements

I am still using the Logitech C615 USB webcam plugged into a Pi 3 B. Previous [HomeKit post](/Adding-A-Webcam-To-HomeKit/) covers installation of required software and system components in Raspbian.

### Updated Settings in `config.json`

{% gist 613bfb96c3e66544a34662dbb2f9b4e2 %}

**Notable changes**:

 - there is now an explicit "`stillImageSource`" that turns some `ffmpeg` knobs to improve reliability of snapshots.
 - the `re` switch is for "real-time" style streaming that is useful if the source stream is a file, in this case `/dev/video0`
 - "`videoProcessor`" is a local built-from-source `ffmpeg` binary. This is not necessary as the `ffmpeg` binary available in Raspbian _stretch_ has all the required runtime configs.


### Using `systemd` to Start `homebridge` on Bootup

Using instructions at [Running Homebridge on a Raspberry Pi](https://github.com/nfarina/homebridge/wiki/Running-HomeBridge-on-a-Raspberry-Pi#running-homebridge-on-bootup-systemd) for **Running Homebridge on Bootup (systemd)** there is a `homebridge.service` file that was already installed.

{% gist 0765555572efac6929e7cfbf022db14d homebridge.service %}

#### Test changes to `config.json` for `homebridge` running under `systemd`

```shell
sudo systemctl restart homebridge
sudo journalctl -f -u homebridge | less -F
```

Press <kbd>Ctrl-C</kbd> to stop live log file streaming and <kbd>q</kbd> to quit `less`

See previous posts for more debugging ideas if problems are encountered.

## What it looks like?

In `Home.app` "[Home]" tab, if you have the camera designated as a "Favorite"

![main_screen_webcam](/images/2018-08-25-Favorite-cameras.jpg)

### References

- GitHub project hosting the `homebridge-camera-ffmpeg` homebridge plugin
	- [https://github.com/KhaosT/homebridge-camera-ffmpeg/](https://github.com/KhaosT/homebridge-camera-ffmpeg/)
    - Wiki there on [Raspberry Pi](https://github.com/KhaosT/homebridge-camera-ffmpeg/wiki/Raspberry-PI)

- GitHub project of `homebridge`
    - [https://github.com/nfarina/homebridge](https://github.com/nfarina/homebridge)
    - Wiki there on [Running Homebridge on Raspberry Pi](https://github.com/nfarina/homebridge/wiki/Running-Homebridge-on-a-Raspberry-Pi)

- Previous blog posts
   - [HomeKit connecting to Nest thermostat and Belkin WeMo devices](/Extending-HomeKit-with-Homebridge-and-Raspberry-Pi/ "Extending HomeKit with Homebridge and Raspberry Pi to All the Things")
   - [Adding a Webcam to Homekit Using a Raspberry Pi 3](/Adding-A-Webcam-To-HomeKit/ "Getting a USB Webcam to work with Homebridge")
