---
layout: post
title: Multi-Monitor Weird Tricks in Linux
date: 2020-03-26
mathjax: False
comments: False
image: /images/dual-display-intel-after.png
---

Using different Linux systems with a dual-monitor setup has been out frustrating, especially with the physical LCD monitors using different pixel resolutions. Now I have some (non-foolproof) ways from command line under Linux to set their resolutions.

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->

-	[A note about my setup](#a-note-about-my-setup)
	-	[Graphics Development](#graphics-development)
	-	[Nvidia graphics card dual-monitor script](#nvidia-graphics-card-dual-monitor-script)
	-	[Intel integrated graphics dual-monitor script](#intel-integrated-graphics-dual-monitor-script)

<!-- markdown-toc end -->

A note about my setup
---------------------

Two monitors, each **27 inch**, positioned side-by-side on small riser stands

-	Monitor 1: 2560x1440 (1440p), Using HDMI connection (*through HDMI switch*\)
-	Monitor 2: 3840x2160 (4K), Using DisplayPort connection (*through DP+USB KVM switch*\)

I prefer running both external monitors at 1440p resolution. Since both monitors are approximately the same physical dimensions, moving applications across monitors set to the same resolution works seamlessly. There are no "gaps" or "walls" when moving the mouse pointer between monitors. No different screen size for fonts. It just makes mork sense to work this way.

For a while, I have been running these connected to a 2015 13-inch MacBook Pro. macOS has excellent multi-display support. macOS recognizes and remembers multiple-display settings and will switch to most recent configuration with clamshell open (built-in LCD + two external displays) or closed (two external displays). It knows about and presents the full complement of native and scaling resolutions for each monitor in System Preferences -> Displays applet.

### Graphics Development

I recently purchased an Nvidia graphics card and started learning about computer graphics programming. I installed the card in a desktop computer that boots Linux or Windows. The system is what I used to develop the raytracing, CUDA, OptiX and Vulkan repos on my GitHub. And I prefer to do this type of development in Linux.

And it so happens that Vulkan development is even (mostly) supported on an Intel integrated graphics CPU that is seven years old at this point, and I am using that system to write this post.

Two systems:

-	System 1 (hostname `vader`\): Intel i7-4960X CPU, RTX 2070 Super graphics card
-	System 2 (hostname `yoda`\): Intel i7-4770k CPU, HD 4600 integrated graphics

The scripts are for running on recent Ubuntu Linux (19.10 or 20.04). Windows 10 drivers seem to encounter similar issues, but will not be covered below.

Nvidia graphics card dual-monitor script
----------------------------------------

After iterating with this for way too long, I finally was able to reliably set both monitors to desired configuration from command line. Originally I could only get the `nvidia-settings` under Linux (which comes with the nvidia driver) to change the resolution.

Ultimately, the incantation was determined by checking the Xorg.log file to see what appeared when the `nvidia-settings` applet changed the resolutions, and trying various partially documented strings in nvidia driver manpages.

[set_vader_desktop_resolution.sh](https://github.com/idcrook/i-dotfiles/blob/master/homedir/bin/linux/set_vader_desktop_resolution.sh)

```shell
#!/bin/sh -x

nvidia-settings --assign CurrentMetaMode="HDMI-0: nvidia-auto-select +2560+0 {ViewPortIn=2560x1440, ViewPortOut=2560x1440+0+0}, DP-0: nvidia-auto-select +0+0 {ViewPortIn=2560x1440, ViewPortOut=3840x2160+0+0}"

# for some reason the X server does this instead, offsetting the viewport for the second screen (screen on  the right):
# Setting mode "HDMI-0: nvidia-auto-select @2560x1440 +3840+0 {ViewPortIn=2560x1440, ViewPortOut=2560x1440+0+0}, DP-0: nvidia-auto-select @2560x1440 +0+0 {ViewPortIn=2560x1440, ViewPortOut=3840x2160+0+0}"
# the +3840 is a problem
```

Intel integrated graphics dual-monitor script
---------------------------------------------

The integrated graphics system presented another problem. The Gnome desktop Settings -> Displays applet does not present the 1440p option (2560x1440) as a choice for the 4K monitor.

![Displays system settings, before xrandr commands](/images/dual-display-intel-before.png "before running the xrandr commands")

Fortunately, the Intel driver seems to play nice with `xrandr`, a utility that is designed to deal with multiple monitors and resolutions and the like. And new modes added with it even show up in the Displays applet. It's not necessary to use Displays control panel once the command line script has been run, but it is interesting to me to note that.

[set_yoda_desktop_resolution.sh](https://github.com/idcrook/i-dotfiles/blob/master/homedir/bin/linux/set_yoda_desktop_resolution.sh)

```shell
#!/bin/bash -x

# Using output from # cvt 2560 1440 60
xrandr --newmode "2560x1440_60.00"  312.25  2560 2752 3024 3488  1440 1443 1448 1493 -hsync +vsync
# the next line may error if mode is already defined
xrandr --verbose --addmode DP-1 "2560x1440_60.00"
xrandr  --output DP-1 --mode "2560x1440_60.00" --left-of HDMI-1

# xrandr --listmonitors
# Monitors: 2
#  0: +*DP-1 2560/600x1440/330+0+0  DP-1
#  1: +HDMI-1 2560/597x1440/336+2560+0  HDMI-1
# xrandr --verbose --listproviders
```

![after running the xrandr commands](/images/dual-display-intel-after.png "after running the xrandr commands")
