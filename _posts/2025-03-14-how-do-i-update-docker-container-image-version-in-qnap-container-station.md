---
layout: post
title: How Do I Update Docker Container/Image Version in QNAP Container Station?
date: 2025-03-14
mathjax: False
comments: False
image: /images/{imagepath}
---

I needed to update a service running in docker container ([Pi-hole – Network-wide Ad Blocking](https://pi-hole.net/)) on my QNAP NAS. It is running as a container and not an "app" (`docker compose` in QNAP vernacular) and was originally created by GUI. Googling for how to do using the QNAP QTS Container Station GUI only worked for apps. I eventually have figured out a general way to do what I need, using command line docker on the QNAP.

## Recreating a container?

It turns out there is no way in the QNAP Container Station web app GUI to "recreate" a container with the updated-to-latest-version image. Annoyingly, this works as desired in the "Apps" area of Container Station, but those are based on `docker compose` services and not the more simple single container.


Container Station loses track of which image is allocated to your container if you manually pull an image in Images interface-- and then disables the "Re-create" item for the container.  However, if you "re-create" the container, thinking it will pull the `latest` tagged image and use that for your "re-created" container, you'd be mistaken. It just re-uses the existing (older) image.


## Using Virtual Networking in Container Station

It turns out that Container Station is syntactic sugar around a standard Linux docker install. It knows how to map filesystem shares, special networking, and subset of devices to services or containers. Understanding this is key to being able to update image version for existing container.

### Needing a static IP on home LAN for `pi-hole`

I started using `pi-hole` on home LAN, and the simplest way to enable it on all network clients is by using  `pi-hole` server as DNS server. How this works: `pi-hole` server IP is added as a manually specified DNS server on router. Then, when the router issues DHCP assignments, it includes `pi-hole`'s IP as list of DNS servers provided to clients.

For this to work, `pi-hole` server IP should be well-known, i.e., static DHCP reservation.  And for that to work, the MAC address of pi-hole server needs to be set in router DHCP reservation table so that it assigns the static IP to pi-hole service/server.

In our scenario, the pi-hole server is really only a docker container running at a virtualized network address managed by the NAS. It can be used to assign multiple unique IPs to docker container services, since it is a virtualized IP. and it uses a QNET interface -- something specific to QNAP Constainer Station and docker implementation.  I was not able to determine how to reliably configure the QNET interfaces, so I had container station do it for me!

It's simply a process of using Container Station container UI to create the desired container, setting your required environment variables, and including host networking found in Advanced configuration, where a virtual interface with corresponding randomly-chosen MAC address can be allocated.

![including host networking found in Advanced configuration <>](/images/container_advanced_networking_host.png "Including host networking found in Advanced configuration")

## Using docker CLI and some utilities to update version


### Figure out docker command line used to create image


### Trim and Fill in any missing pieces in command line


## Summary
