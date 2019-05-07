---
layout: post
title: Emacs27 on macOS - Now (Again❓) With Emoji!‼️
date: 2019-05-07
mathjax: False
comments: False
image: /images/company-emoji-suggest_sm1.png
---

I have been refreshing my emacs config as part of [i-dotfiles](https://github.com/idcrook/i-dotfiles), and had made a note to add emoji support.  After googling, I remembered emacs maintainers intentionally disabled multi-color font support used in macOS for native emoji support. Then, a git commit [Update multicolor font support status](http://git.savannah.gnu.org/cgit/emacs.git/commit/etc/NEWS?id=28220664714c50996d8318788289e1c69d69b8ab) in Sacha Chua's [2019-04-29 Emacs news](https://sachachua.com/blog/2019/04/2019-04-29-emacs-news/) surfaced. Using `company-emoji` and the re-enabled upstream support, emojis are back in Emacs27.

## Building Emacs From Source

For years I have used the `emacs` cask from homebrew, which installs `Emacs.app` from the `.dmg` published at <https://emacsformacosx.com/> (currently emacs: 26.2). Rather than roll my own yet-another build-emacs-from-source script, I decided to use [daviderestivo/homebrew-emacs-head](https://github.com/daviderestivo/homebrew-emacs-head) repo/homebrew tap[^1].

It couldn't have been much easier:

```shell
# first, rename existing /Applications/Emacs.app -> Emacs26.app
brew tap daviderestivo/emacs-head
brew install emacs-head --HEAD --with-cocoa --with-imagemagick --with-jansson
ln -s /usr/local/opt/emacs-head/Emacs.app /Applications
```

This built emacs from source using its *master* git branch. It is the "NS"/cocoa version I prefer. (`jansson` is C-lang JSON parser). The symlink-to-`/Applications` snippet was straight out of the **Caveats** message in its Homebrew output.

The `homebrew-emacs-head` recipe can also be configured to build a emacs26 version with multi-color font support patch, but I figured I would try the emacs27/HEAD code.



## Configure emacs startup files

I now (as of this last week) have my `.emacs.d` startup files in a public github repo. [Here](https://github.com/idcrook/.emacs.d/blob/bb05f12d63a4e7753c1585938fc76d3142aea105/elisp/base-platforms.el#L167-L174) is the code that enables the macOS (`system-type`: `'darwin`) emoji font in Emacs (gist follows)

{% gist 9eef475e0addc019f241850d92cfd763 %}

I don't now if this is the exact appropriate code, but it is working for me. It basically lets emacs know that it can use the `Apple Color Emoji` font.

Also, to get the github-style **:named:** emoji suggestions, code adding `company-emoji`[^2] as an [installed package](https://github.com/idcrook/.emacs.d/blob/bb05f12d63a4e7753c1585938fc76d3142aea105/elisp/base-extensions.el#L122) and to [company-backends](https://github.com/idcrook/.emacs.d/blob/bb05f12d63a4e7753c1585938fc76d3142aea105/elisp/base-extensions.el#L113) is used. Something like:

```elisp
;;; https://github.com/dunn/company-emoji
(use-package company-emoji)
```
and

```elisp
(use-package company
  :config
  ;; ...
  (add-to-list 'company-backends 'company-emoji)
```

❤️


## Running Emacs27 with `company-emoji`

Launching the new `Emacs.app` [as usual](https://github.com/idcrook/i-dotfiles/blob/master/homedir/bin/macos/Emacs.sh), now the *emoji*-s in a file are visible! And if the colon-preface names a la Github web-editing are typed:

```
TBD :smi
```

you can select your completion suggestion from the `company` dropdown:

![](/images/company-emoji-suggest_sm1.png)


which results in the selected emoji (the actual Unicode emoji, not the :colon:-named one) getting inserted into your buffer:

```
TBD 😄
```

Enjoy 🍰️

[^1]: Found on emacs subreddit : [Now that Homebrew has removed build options, how do I get Imagemagick support for emacs on Mac OS?](https://www.reddit.com/r/emacs/comments/bhjtf9/now_that_homebrew_has_removed_build_options_how/eltls2l?utm_source=share&utm_medium=web2x)

[^2]: <https://github.com/dunn/company-emoji>
