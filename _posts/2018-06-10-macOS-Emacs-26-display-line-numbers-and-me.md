---
layout: post
comments: false
title: macOS Emacs 26 display-line-numbers, neotree and me, or How I Became an Emacs Power User Today
date: 2018-06-10
image: /images/neotree-with-line-numbers-meta.png
---

I've been reviving my GNU Emacs config as part of becoming a more active daily user. I typically use a macOS workstation, sometimes connecting to Linux machines (tramp/ssh). The release of [Emacs 26.1](https://github.com/emacs-mirror/emacs/blob/master/etc/NEWS.26) about a week ago gave me additional impetus to consume `Emacs`'s  **customizable, extensible** goodness.

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->

- []() **Table of Contents**
    - [`display-line-numbers`](#display-line-numbers)
    - [`neotree` and `display-line-numbers` out of the box](#neotree-and-display-line-numbers-out-of-the-box)
    - [The Process of Getting `neotree` and `display-line-numbers` to Play Nice Together](#the-process-of-getting-neotree-and-display-line-numbers-to-play-nice-together)
    - [Finally SUCCESS...](#finally-success)
      - [BEGIN_UPDATE 2018-Sep-18](#begin_update-2018-sep-18)
      - [END_UPDATE 2018-Sep-18](#end_update-2018-sep-18)
    - [Conclusion](#conclusion)
- [Footnotes](#footnotes)

<!-- markdown-toc end -->


## Background

The origins of my current emacs config[^1] are from [Emacs Bootstrap](http://emacs-bootstrap.com). I forget exactly when I first declared "Emacs bankruptcy" and started over with the emacs-bootstrap files as a template. Originally I tried a `helm`-based completion setup but `helm` never really clicked with me.

In my most recent overhaul, I have switched to `counsel`, `ivy`/`swiper`,  and `company` for completions. And I am coming around to using `projectile` and its related packages. `projectile` helps me with myriad  Git clones, including on remote hosts.

`tramp` is the greatest thing including the proverbial Emacs kitchen sink, BTW! :kissing_smiling_eyes:

### `display-line-numbers`

Any way, this tidbit from the NEWS file caught my eyes:


```text
** Emacs now supports optional display of line numbers in the buffer.
This is similar to what 'linum-mode' provides, but much faster and
doesn't usurp the display margin for the line numbers.  Customize the
buffer-local variable 'display-line-numbers' to activate this optional
display.  Alternatively, you can use the 'display-line-numbers-mode'
minor mode or the global 'global-display-line-numbers-mode'.  When
using these modes, customize 'display-line-numbers-type' with the same
value as you would use with 'display-line-numbers'.

Line numbers are not displayed at all in minibuffer windows and in
tooltips, as they are not useful there.

Lisp programs can disable line-number display for a particular screen
line by putting the 'display-line-numbers-disable' text property or
overlay property on the first character of that screen line.  This is
intended for add-on packages that need a finer control of the display.

Lisp programs that need to know how much screen estate is used up for
line-number display in a window can use the new function
'line-number-display-width'.

'linum-mode' and all similar packages are henceforth becoming obsolete.
Users and developers are encouraged to switch to this new feature
instead.
```

So **Emacs 26** has deprecated `linum-mode`...

Side note: filed an [issue](https://github.com/tom-tan/hlinum-mode/issues/5) for [hlinum-mode](https://github.com/tom-tan/hlinum-mode) since it works with `linum-mode` but does not work with Emacs 26 `display-line-numbers.el`. It was closed with a "not going to fix", as apparently the hooks that it had relied on are gone with the new, preferred-in-Emacs-26 way.

### `neotree` and `display-line-numbers` out of the box

I have been using [neotree](https://github.com/jaypei/emacs-neotree) package, which I would describe as a "sidebar and dired in one".  It can work with `projectile` and so is a nice way to navigate and grok fresh projects.

Since everything in Emacs is "just a buffer", `neotree` hadnt yet been updated to work with the `display-line-numbers` hotness new in Emacs 26. So it looked like this with `(global-display-line-numbers-mode 1)`:

![neotree with line numbers fail](/images/neotree-with-line-numbers.png "neotree with line numbers")

Note the line numbers being included on the left side of the image, in the `neotree` buffer.

### The Process of Getting `neotree` and `display-line-numbers` to Play Nice Together

No problem. I knew that `neotree` already had a hook allowing this behavior to be overridden. In fact, this same hook was the way to turn off `linum-mode` numbering (the pre-Emacs 26 way) in `neotree`[^2].  Lemme just use the same hook, `neo-after-create-hook`...

```emacs-lisp
(defun display-line-numbers-disable-hook ()
  "Disable display-line-numbers locally."
  (display-line-numbers-mode -1))


;; Disable line-numbers minor mode for neotree
(add-hook 'neo-after-create-hook 'display-line-numbers-disable-hook)
```

Problem solved, right? _No.  Got an error_ in the emacs `mode-line` (mode-line status text is impossible to copy directly to system clipboard, BTW):

``` text
Wrong number of arguments: (lambda nil "Disable display-line-numbers locally." (display-line-numbers-mode -1)), 1
```

I am by no means expert in `emacs-lisp` but have been reading about it and trying to understand basic functionality. Maybe I was creating the function for the hook wrong? After some googling, I thought that this related form might work:

```emacs-lisp
(add-hook 'neo-after-create-hook (lambda () (display-line-numbers-mode -1)))
```

_Nope.  Got the same error! What is going on?_
...looking further at the error in the `*Messages*` buffer...

```text
run-hook-with-args: Wrong number of arguments: (lambda nil (display-line-numbers-mode -1)), 1
```

OK. This might be a helpful clue? The function being called is `run-hook-with-args`, but my `hook` functions didn't expect any arguments.

__**Some more googling**__

The emacs manual says that `run-hook-with-args` is a less common way to implement hooks. Tracing `neo-after-create-hook` into the `neotree.el` source I arrived at:

```emacs-lisp
(run-hook-with-args 'neo-after-create-hook '(window))
```

It turns out `neotree` was passing a `'(window)` argument to the hook function(s).

## Finally SUCCESS...

So all I really needed was a `hook` function that could accept another argument to its invocation. OK, I just need to add this to my `hook` function. I remember seeing `&optional` all over the place in the emacs manual info browser in function call signatures. I'll just use one of those:

```emacs-lisp
;; Disable line-numbers minor mode for neotree
(add-hook 'neo-after-create-hook (lambda (&optional dummy) (display-line-numbers-mode -1)))
```

:thumbsup: SUCCESS!

![neotree without line numbers success](/images/neotree-without-line-numbers.png "neotree without line numbers")

 For the full config I use for `neotree` on Emacs 26 and `global-display-line-numbers-mode`:

{% gist 3a0f33b7dc8cba1dbd4d26959f48dd9b use-package_neotree.el %}

#### BEGIN_UPDATE 2018-Sep-18

After this post made it on [reddit](https://www.reddit.com/r/emacs/comments/9gjb0s/how_to_hide_line_numbers_in_neotrees_buffer/) and Sacha Chua's [weekly news](http://sachachua.com/blog/2018/09/2018-09-17-emacs-news/), there was a suggestion on how to use an [established Emacs Lisp idiom](https://www.reddit.com/r/emacs/comments/9gjb0s/how_to_hide_line_numbers_in_neotrees_buffer/e64jfkf/) in this context.

Instead of

```emacs-lisp
;; original post had this
(lambda (&optional dummy) ...
```
a better way would be
```emacs-lisp
;; more idiomatic of emacs
(lambda (&rest _) ...
```
so I've updated the gist.
#### END_UPDATE 2018-Sep-18

# Conclusion

Turns out having all the source code and built-in introspection and help files for your editor, that you can edit, are a "Really Good Idea":exclamation: :thumbsup:

Emacs is like the *infinity editor*.

# Footnotes

[^1]: Sorry, I do not have my dotfiles publicly available. I do have my macOS and Linux configs in a shared git repo, but it is private to me

[^2]: This was before `neotree` itself added native support for recognizing `linum-mode` to turn off these numbers.
