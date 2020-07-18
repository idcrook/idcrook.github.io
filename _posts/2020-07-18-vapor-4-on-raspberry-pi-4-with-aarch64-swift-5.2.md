---
layout: post
title: Vapor 4 on Raspberry Pi 4 With aarch64 Swift 5.2
date: 2020-07-18
mathjax: False
comments: False
image: /images/2020-07-17-vapor4_raspberrypi.png)
---

Using a Raspberry Pi 4 running 64-bit Ubuntu 20.04 (`aarch64` a.k.a. `arm64`)

## Install swift 5.2.4 for aarch64 

Was simple, using the instructions and pre-built packages available at [https://github.com/futurejones/swift-arm64](https://github.com/futurejones/swift-arm64)

```shell
curl -s https://packagecloud.io/install/repositories/swift-arm/release/script.deb.sh | sudo bash
sudo apt-get install swift-lang
swift --version
```

    Swift version 5.2.4 (swift-5.2.4-RELEASE)
    Target: aarch64-unknown-linux-gnu

## Install vapor toolbox

The "simple" build command I found in an earlier examples on the web didn't work, erroring out:

```
$ swift build -c release
```
    Fetching https://github.com/tanner0101/mustache.git
    Fetching https://github.com/vapor/console-kit.git
    Fetching https://github.com/jpsim/Yams.git
    Fetching https://github.com/apple/swift-nio.git
    Fetching https://github.com/apple/swift-log.git
    Cloning https://github.com/apple/swift-nio.git
    Resolving https://github.com/apple/swift-nio.git at 2.19.0
    Cloning https://github.com/apple/swift-log.git
    Resolving https://github.com/apple/swift-log.git at 1.4.0
    Cloning https://github.com/tanner0101/mustache.git
    Resolving https://github.com/tanner0101/mustache.git at 0.1.1
    Cloning https://github.com/vapor/console-kit.git
    Resolving https://github.com/vapor/console-kit.git at 4.2.0
    Cloning https://github.com/jpsim/Yams.git
    Resolving https://github.com/jpsim/Yams.git at 2.0.0
    error: missing LinuxMain.swift file in the Tests directory

> **error: missing LinuxMain.swift file in the Tests directory**

The `error: missing LinuxMain.swift file in the Tests directory` comes from `vapor/console-kit` not having that file.

Fortunately it can still be built. And it is already correct in the docs to build the toolbox..

[https://docs.vapor.codes/4.0/install/linux/](https://docs.vapor.codes/4.0/install/linux/)

```shell
git clone https://github.com/vapor/toolbox.git
cd toolbox
git checkout <desired version>
swift build -c release --disable-sandbox --enable-test-discovery
mv .build/release/vapor /usr/local/bin
```

So, ARMed with this Linux knowledge, the build now is successful (from HEAD of default branch)

```shell
swift build -c release --disable-sandbox --enable-test-discovery
mv .build/release/vapor /usr/local/bin
sudo cp -av .build/release/vapor /usr/local/bin/
whereis vapor
# vapor: /usr/local/bin/vapor
vapor --help
```


## Now build a vapor project

```shell
mkdir -p ~/projects/vapor
cd ~/projects/vapor
vapor new hello -n
cd hello
vapor build 
# ... with start with fetching and building dependencies in Package.swift
```

    Building project...
    Fetching https://github.com/vapor/vapor.git
    Fetching https://github.com/apple/swift-nio.git
    Fetching https://github.com/apple/swift-nio-ssl.git
    Fetching https://github.com/swift-server/swift-backtrace.git
    Fetching https://github.com/apple/swift-crypto.git
    Fetching https://github.com/apple/swift-metrics.git
    Fetching https://github.com/vapor/websocket-kit.git
    Fetching https://github.com/apple/swift-nio-http2.git
    Fetching https://github.com/vapor/async-kit.git
    Fetching https://github.com/apple/swift-log.git
    Fetching https://github.com/vapor/console-kit.git
    Fetching https://github.com/vapor/routing-kit.git
    Fetching https://github.com/swift-server/async-http-client.git
    Fetching https://github.com/apple/swift-nio-extras.git
    ...
    [1412/1412] Linking Run
    Project built.

## And run the server

```shell
vapor run serve
```

> [ NOTICE ] Server starting on http://127.0.0.1:8080

and,  in another terminal,  send some requests

```shell
curl localhost:8080
```

> `It works!`

```shell
curl localhost:8080/hello
```

> `Hello, world!`


```shell
curl localhost:8080/non-existent
```

> `{"error":true,"reason":"Not Found"}`

```shell
curl -I localhost:8080/hello
```

> HTTP/1.1 200 OK

    content-type: text/plain; charset=utf-8
    content-length: 13
    connection: keep-alive
    date: Sat, 18 Jul 2020 02:23:11 GMT

![Vapor Server running](/images/2020-07-17-vapor4_raspberrypi.png)