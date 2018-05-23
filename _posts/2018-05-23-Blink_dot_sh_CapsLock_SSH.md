---
layout: post
comments: true
title: Hardware CapsLock as Control key in iOS SSH client using blink.sh
---

I've been searching for a way to use CapsLock as another Control key on iOS for as long as there has been hardware keyboard support in iOS. (Emacs habits never die!)[^1] I have legacy USB and bluetooth keyboards that I’d like this to work with.

[Blink shell](https://itunes.apple.com/us/app/id1156707581?at=1000lwmW "Blink Shell: Mosh & SSH") ([homepage](https://www.blink.sh/)) has a _software_ setting that allows the “CapsLock as Control” behavior. It also has useful features like support for the `mosh` shell (improvement on ssh sessions over flaky connections) and color themes and great font support, including included Powerline-compatible fonts.

## Settings in `blink.sh`

blink app is strange since it presents you with a prompt similar to what you’d encounter in a terminal shell: `blink>`.  To bring up app settings, the command is `config`.

![Bring up config](/images/blink-config-at-prompt.jpeg)

The keyboard-related settings are easy enough to find.

![Settings dialog](/images/blink-dialog-Settings.jpeg)
![Keyboard settings](/images/blink-dialog-Keyboard.jpeg)

Since the app uses a software method to emulate the key-remapping behavior, the CapsLock indicator on actual keyboard still will toggle its light with each press.  Also note that this behavior only works within the app, and doesn’t work across iOS apps or system :frowning: ...

## Available in the App Store

[Blink shell](https://itunes.apple.com/us/app/id1156707581?at=1000lwmW "Blink Shell: Mosh & SSH") is available for a reasonable price in the App Store—it is well worth the value!  It is also open-source, so it’s possible to file issues or build your own version from its open-source repo [on GitHub](https://github.com/blinksh/blink).


[^1]: Many of [Emacs](https://www.gnu.org/software/emacs/) functions and commands are bound to the <kbd>Control</kbd>. Using the location of the <kbd>CapsLock</kbd> key as another <kbd>Ctrl</kbd> key reduces strain in the keyboard hand.
