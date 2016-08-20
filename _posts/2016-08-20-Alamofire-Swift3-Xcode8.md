---
layout: post
title: Alamofire HTTP library with Xcode 8 and Swift 3
---

Had to figure out how to use the Swift 3 branch. Didn't find the instructions elsewhere.

# Build instructions (Swift 3, iOS 10)

Assumes Xcode 8.0 β6, iOS 10 target (with Swift 3), Mac Homebrew with git

 1. Download Alamofire framework using git to get `swift3` branch 

        cd Project  # Xcode project created with git source control
        git submodule add https://github.com/Alamofire/Alamofire.git
        cd Alamofire
        git checkout swift3
        cd ..
        git add Alamofire
        git commit -m "moved Alamofire to swift3 branch"

 1. Follow additional instructions on integrating with Xcode project
   - [Manual instructions](https://github.com/Alamofire/Alamofire/tree/swift3#manually)
 1. Use snippet example below to see that it works!

### Snippet to test Alamofire in AppDelegate

A couple of notes about Swift 3

 - the enum's are lowercase (`.get` instead of `.GET`)
 - provide all argument names in function calls

```swift
//
//  AppDelegate.swift
//

import UIKit
import Alamofire

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?

    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplicationLaunchOptionsKey: Any]?) -> Bool {
        // Override point for customization after application launch.
        Alamofire.request("https://httpbin.org/get", withMethod: .get)
            .responseJSON(completionHandler: {response in
                debugPrint(response.request)
                print(response.response)
                print(response.result.value)
                })
        return true
    }
```

Example output

```
Optional(https://httpbin.org/get)
Optional(<NSHTTPURLResponse: 0x60800002ea40> { URL: https://httpbin.org/get } { status code: 200, headers {
    "Access-Control-Allow-Origin" = "*";
    "Content-Length" = 316;
    "Content-Type" = "application/json";
    Date = "Sat, 20 Aug 2016 14:32:18 GMT";
    Server = nginx;
    "access-control-allow-credentials" = true;
} })
Optional({
    args =     {
    };
    headers =     {
        Accept = "*/*";
        "Accept-Encoding" = "gzip;q=1.0, compress;q=0.5";
        "Accept-Language" = "en-US;q=1.0";
        Host = "httpbin.org";
        "User-Agent" = "Project/com.example.Project (1; iOS 10.0.0)";
    };
    origin = "8.8.8.8";
    url = "https://httpbin.org/get";
})
```

