---
layout: post
title: Update This Blog for Faster macOS Docker Development
date: 2022-03-23
mathjax: False
comments: False
image: /images/enabling-virtiofs-macos.png
---

Using docker on macOS for `jekyll` development has always been slower than other platforms. There are ways to mitigate this, including a recent Docker Desktop update for macOS.

This blog hosted on the GithHub People Pages has been around since 2015. It's always been in a jekyll blog format that works with the GitHub backend that generates the jekyll blog for hosting. I prefer to run jekyll locally to preview posts as I compose them before publishing.

Long ago I discovered for me that this mean running Docker jekyll container locally. The downside of this had been regenerating the site after each edit would take a long time and then I would have to manually reload the page in the browser once it had been regenerated.

Incremental regeneration and LiveReload
---------------------------------------

It turned out to be simple to enable a few features within jekyll to improve the development cycle.

```diff
 docker run --rm \
   --volume="$PWD:/srv/jekyll" \
   --volume="$PWD/vendor/bundle:/usr/local/bundle" \
   -it \
   -p 4000:4000 \
+  -p 35729:35729 \
   jekyll/jekyll:$JEKYLL_VERSION \
-  jekyll serve --force_polling
+  jekyll serve --incremental --force_polling --livereload
```

See [UsingDockerToServe.md](https://github.com/idcrook/idcrook.github.io/blob/main/UsingDockerToServe.md) for additional details on how I run a jekyll docker container.

#### Live Reload

I think the LiveReload feature has been built-in to `jekyll` for years, and I am not sure why I never used it. Perhaps it was broken with Docker on Mac or some other similar reason I don't recall. Anyway, enabling it takes one of the annoying pieces of previewing edits: reloading the page once the regenerated one is ready. It's an additional command line switch (`--livereload`) to `jekyll serve` and exposing the port `35729` from the container that is used to communicate the live-reload magic with the browser. These changes are highlighted in the `docker run` snippet.

#### Incremental

The command line switch `--incremental` is more obvious, as the `jekyll serve` command itself would message about it while it was starting up. There is a gotcha with it as it doesn't seem to regenerate the main index pages unless a new post markdown file is added to the directory.

This annoyance can be circumvented by stopping the docker run and re-running it without the incremental switch to re-generate full website. Since pages are editing much more often than they are added, this isn't too big of a deal, and the incremental way can be the default.

Docker Desktop 4.6 for Mac
--------------------------

One other thing related to macOS Docker performance is the `VirtioFS` layer added very recently to Docker Desktop for Mac. It's still classified as *Experimental* but it promises great improvements for file consistency across host/container files. Enabling it on an Intel silicon Mac requires macOS 12.3, so it's all quite fresh.

![enabling Virtiofs <>](/images/enabling-virtiofs-macos.png "Instructions for enabling Virtiofs in Docker Desktop")

Via <https://docs.docker.com/desktop/mac/#experimental-features>: "Enable VirtioFS"

[Speed boost achievement unlocked on Docker Desktop 4.6 for Mac - Docker](https://www.docker.com/blog/speed-boost-achievement-unlocked-on-docker-desktop-4-6-for-mac/)

Results
-------

I don't have very good controls for before/after data, but it has been a greatly perceptible improvement. This used to take around 20 seconds on my 2015 13-inch MBP. Now it is more like 5 seconds.

```
Regenerating: 1 file(s) changed at 2022-03-23 21:03:54
                    _posts/2022-03-23-update-this-blog-for-faster-macos-docker-development.md
       Jekyll Feed: Generating feed for posts
                    ...done in 4.390487499 seconds.
```
