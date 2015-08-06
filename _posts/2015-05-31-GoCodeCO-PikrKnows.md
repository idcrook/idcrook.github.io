---
layout: post
title: GoCode Colorado 2015 and Pikr Knows
---

I have been busy the past few weeks, as system architect and full-stack developer on the [winning GoCode Colorado 2015 team](http://blogs.denverpost.com/tech/2015/05/22/go-code-colorado-when-big-data-developers-and-government-collide/17286/), with our app named [Pikr Knows](http://pikrknows.com).  I also came up with its name, which seems to be easy to remember...


## What is Pikr Knows?

What is *Pikr Knows*? Its origin was an app that was built to address the Tourism category in the [GoCode Colorado 2015](http://gocode.colorado.gov/) Challenge.

![PikrKnows logo](/images/PikrKnows_logo.png)

It is about activity discovery in Colorado, and it can use your user preferences in its searches.

You can [sign up and start using the app](http://pikrknows.com) today.


## Some Technical Details of Pikr Knows implementation

From a high-level point-of-view, [Pikr Knows](http://pikrknows.com) is a webapp based on the [MEAN stack](http://meanjs.org/) (MongoDB Express Angular.js Node.js). For location-based searches, the high-quality, open-source [postGIS](http://postgis.net/) database is used.  [http://pikrknows.com](http://pikrknows.com) itself serves through a [NGINX](http://wiki.nginx.org/Main)-based proxy.

Using [node.js](https://nodejs.org/) means that JavaScript code is everywhere, including the server code. This relationship, coupled with the JSON-document oriented [mongoDB](https://www.mongodb.org/), makes it pretty seamless to get data back-and-forth from the server to the client.

Git is awesome, by the way, in case you didn't already know that, and so is SSH. 


## What is next?

Our team has many planned feature improvements and updates ahead of us for our users. Some of these improvements are based on feedback from users and others are things we just were not able to roll out yet.  Stay tuned!
