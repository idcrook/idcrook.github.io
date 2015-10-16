---
layout: post
title: RStudio and rJava on OS X El Capitan
---

## Intro to Data Science

I recently started an [Intro to Data Science Workshop](https://www.mysliderule.com/workshops/data-science) and today in our weekly mentor meeting, my mentor and I were running and interactive session in RStudio. He asked my to install a package<sup id="FSelector1">[1](#footnote1)</sup> in `R` so we could look at distinct factors in the `iris` dataset.

The `install.packages("FSelector1")` was unsuccessful, as packages *it* depended on were Java based, and I didn't have java, or the `rJava` package, installed on my MacBook Pro running OS X El Capitan. I told him I would take care of that after we were done with our call.  And so began my descent into a eventually fruitful yak-shaving exercise...


## Java, OS X El Capitan 10.11, and R (Arrrgggh!)

I googled, and then installed to the latest Java SDK from Oracle (`jdk-8u60-macosx-x64.dmg`), as that is what the first couple links prescribed.  Easy enough.

Now I tried to install `rJava` in `Rstudio`.

``` {r}
install.packages('rJava')
```

It failed to install, with an error. The error was this when tring to install the `rJava` package, which is a dependency for any other `R` package implemented in Java:

```
...
interpreter : '/usr/bin/java'
archiver    : '/usr/bin/jar'
compiler    : '/usr/bin/javac'
header prep.: '/usr/bin/javah'
cpp flags   : '-I/Library/Java/JavaVirtualMachines/jdk1.8.0_60.jdk/Contents/Home/jre/../include'
java libs   : '-L/Library/Java/JavaVirtualMachines/jdk1.8.0_60.jdk/Contents/Home/jre/lib/server -ljvm'
checking whether Java run-time works... yes
checking whether -Xrs is supported... yes
checking whether JNI programs can be compiled... yes
checking JNI data types... configure: error: One or more JNI types differ from the corresponding native type. You may need to use non-standard compiler flags or a different compiler in order to fix this.
ERROR: configuration failed for package ‘rJava’
* removing ‘/usr/local/lib/R/3.2/site-library/rJava’
* restoring previous ‘/usr/local/lib/R/3.2/site-library/rJava’
```

the specific message was:

```
checking JNI data types... configure: error: One or more JNI types differ from the corresponding native type. You may need to use non-standard compiler flags or a different compiler in order to fix this.
```

There were many sources that had different accounts for what was wrong.  They variously had me installing different versions or java, setting environment variables, running RStudio from the command line with special invocations, and variants of each. After attempting various of these fixes, I realized that many of them were solutions that had to do with OS X Yosemite, and not El Cap.

I instead started looking specifically for El Capitan, and found something that led to me getting it working.



## What finally worked

``` {bash}
ln -f -s $(/usr/libexec/java_home)/jre/lib/server/libjvm.dylib /usr/local/lib
```

### Details of the first part

The [original source where I found this](https://chisqr.wordpress.com/2015/10/01/rjava-load-error-in-rstudior-after-upgrading-to-os-x-el-capitan/) prescribed `sudo` on the `ln`.  It pointed out that this was a [change from OS X Yosemite](http://stackoverflow.com/questions/30738974/rjava-load-error-in-rstudio-r-after-upgrading-to-osx-yosemite) to point to `/usr/local/lib` due to SIP feature (System Integrity Protection) added in El Capitan (`/usr/local/` is not subject to restrictive SIP constraints).

`sudo` is not strictly required if you use [Homebrew](http://brew.sh/) under Mac OS X El Capitan as the current user. Everything under `/usr/local` is owned by the current user in that scenario, including my `R` and `rstudio` cask intalled from Homebrew.

After adding that symlink, `rJava` installed fine, using the Oracle JDK 1.8 Now to get back to the original point: Install `FSelector`.

Even though `rJava` library was not installed, installation would **still error**, and an OS dialog would pop-up saying I needed to install Java.  **WTF?!**

More googling.

### Install Java 6 workaround.

Due to an issue with Oracle JDK 1.8 on Mac OS X, there is a need to install the "old" JRE 1.6 from Apple to have it detect `java` being installed.  Awesome!

- [https://github.com/s-u/rJava/issues/37](https://github.com/s-u/rJava/issues/37)

Here's that Apple-hosted JRE 1.6 installer: [Java for OS X 2015-001](https://support.apple.com/kb/DL1572?locale=en_US)

Now after installing that, the `R` packages that had a dependency on `java` finally installed themselves without errors.  Now what was doing this for? ... Oh, yeah.  Analysing some `iris` data.

![scatterplot of petal dimensions](/images/iris_petal_LXW_scatter.jpeg)

## Footnotes





<b id="footnote1">1</b> FSelector package from [CRAN](https://cran.r-project.org/web/packages/FSelector/index.html) [↩](#FSelector1)
