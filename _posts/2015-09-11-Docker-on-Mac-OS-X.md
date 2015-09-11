---
layout: post
title: Docker on Mac OS X
---

A problem I ran into after installing OS X El Capitan GM on my Mac mini
[colocated in Las Vegas](http://macminicolo.net): it became unreachable after
the install. I filed a ticket and got prompt help from the support staff at
MacMiniColo! It appears that the installer decided to throw away all my network
settings, and switch to a default of assigning IP through DHCP-- which doesn't
really work when you are bare on the Internet.

Anyway, it gave me a chance to inspect some of the Docker containers and their
resource usage under OS X.

## Polling for live updates

Polling the filesystem is resource intensive. It can consume extra CPU when
other types of notification techniques that something changed consume less My
Mac mini in the cloud was breathing fire and running *~90C*, which is not a
good thing.


### Fixing the MEAN polling

One of my sites is running a [MEAN](http://meanjs.org) stack-based site on my
website.  It is a [node.js](https://nodejs.org/en/) server and I run it on a
Docker container, serving up the site in "production" mode.

The problem with this is that it was still running a polling filesystem watcher
that looks at all the files inspecting for changes.  However, in production,
you are not needing to live-reload your local edits; you push the changes to a
repository, and pull them to deploy.

It was a simple enough edit to change the `gruntfile.js` to take the `watch`
task off the `concurrent` in a new *production* setting.  I made the changes
and pushed them to the git repository.  And at the server, I pulled and
restarted the docker container that runs the node.js server.  No change.  It
was still watching.

**Huh**?  Oh- it is because the `gruntfile.js` was not visible in the
container.  When I built the container, it added all the files, but now, they
are not mounted in the running docker image.

Fortunately, Docker allows a simple way to add a file as a volume into the
container.

```
-v $PWD/gruntfile.js:/home/mean/gruntfile.js \
```

Relaunching the container with this added to its invocation, and the watcher no
longer ran.  Here is a pointer to the original
[gruntfile](https://github.com/meanjs/mean/blob/master/gruntfile.js).

### More polling problems: jekyll auto-regenerate


`jekyll` can be used to watch when source files change, and automatically
regenerate the static output HTML that gets served.  This is great, if you have
your website posts in Markdown files, and when you push another post to the git
repository that you store your blog in, it automatically updates the website
HTML that gets served.  GitHub Pages works this way, using jekyll behind the
scenes.  Originally I couldn't get this to work with my container.  After some
some googling, I discovered why.

Unfortunately, Docker on OS X has to go through an extra layer of running a VM
and using vboxsf from VirtualBox do its magic to communicate with its host.  It
cannot/doesn't use `inotify` or other such event-based notifications.  To get
it to works, it was shown that adding `--force_polling` to jekyll's serve
command could get this to work. But having this there ends up using a bunch of
CPU resources.

Went from:

```
docker run --rm --label=jekyll --label=pages --volume=$(pwd):/srv/jekyll   -t -p 4000:4000 jekyll/pages jekyll serve --force_polling
```

to

```
docker run -i --rm --label=jekyll --label=pages --volume=$(pwd):/srv/jekyll   -t -p 4000:4000 jekyll/jekyll:pages jekyll serve
```

How did I do that? I just found today a nifty little project geared to helping
with exactly this problem called
[docker-osx-dev](https://github.com/brikis98/docker-osx-dev).  It set's up an
`rsync` tunnel that runs in the boot2docker image that is being used as the
Docker host on OS X.


## Summary

Now, after looking in the VboxHeadless process that my docker containers were
running under, it was running with around 70% less CPU activity than before.
Another hot problem solved.


