---
layout: post
title: .local Networking with ATS in iOS 10
---

Discovered today that in iOS 10, `NSAppTransportSecurity` adds a new exception key for `.local` domain accesses.


# .local Networking

`.local` are Bonjour networking names given to local network services.  OctoPi is configured to advertise its interface using Bonjour.  For example, a fresh install of OctoPi will appear on home network at *http(s)://**octopi.local*** when it boots up. It uses Bonjour networking to make this work.

For App Transport Security (*ATS*)-- required to be enabled on iOS 10 apps and App Store listings starting in 2017-- network access has to be over Transport Laver Security (TLS) to public Internet addresses. "Proper" TLS requires webserver key to be signed by a recognized certificate authority.

Unfortunately, OctoPrint (and many other home networking devices) "self-sign" their certificates.  Self signing can cause ATS to fail unless arbitrary network load accesses are excepted, which kinda defeats the purpose of ATS.  The new allowance is for .local networking only, and doesn't require app to allow arbitrary accesses.

I added the new (new for iOS 10) `NSAllowsLocalNetworking` key to `NSAppTransportSecurity` section in `Info.plist` for my iOS app, and the networking accesses (via **https://** BTW) **still work**, without generating an error!  This new key is documented in the pre-release docs, and I first found mention of it in Apple's Dev Forums.

 - Dev Forum Post: [App Transport Security and local networking](https://forums.developer.apple.com/thread/6205)

It wasn't yet appearing in the helpful dropdowns in the Plist editor in Xcode 8.0 ß6, so I manually added it into the xml.

```xml
	<key>NSAppTransportSecurity</key>
	<dict>
		<key>NSAllowsLocalNetworking</key>
		<true/>
	</dict>
```

## More macOS Bonjour command line discovery

I've included a transcript of commands you can run on macOS to explore some of the information in Bonjour netowrking. My example shows the name for an OctoPi instance and how to get its name and IPv4 address.

```
$ dns-sd -B _http._tcp. local.

Browsing for _http._tcp..local.
DATE: ---Mon 29 Aug 2016---
12:01:34.907  ...STARTING...
Timestamp     A/R    Flags  if Domain               Service Type         Instance Name
12:01:35.248  Add        3   7 local.               _http._tcp.          OctoPrint instance on octopi
^C

$ dns-sd -L "OctoPrint instance on octopi" _http._tcp. local.
Lookup OctoPrint instance on octopi._http._tcp..local.
DATE: ---Mon 29 Aug 2016---
12:35:13.880  ...STARTING...
12:35:14.187  OctoPrint\032instance\032on\032octopi._http._tcp.local. can be reached at octopi.local.:80 (interface 7)
 path=/

$ dns-sd -q octopi.local. A
DATE: ---Mon 29 Aug 2016---
12:35:46.171  ...STARTING...
Timestamp     A/R Flags if Name                          Type  Class   Rdata
12:35:46.172  Add     2  7 octopi.local.                 Addr   IN     10.0.1.46 
```


