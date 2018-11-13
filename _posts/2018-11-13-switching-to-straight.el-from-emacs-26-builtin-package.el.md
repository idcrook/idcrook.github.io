---
layout: post
title: Switching to straight.el from Emacs 26 builtin package.el
date: 2018-11-13
mathjax: False
comments: True
---

On switching to `straight.el` from Emacs 26 builtin `package.el`

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Why switch?](#why-switch)
- [The process of changing over to `straight.el`](#the-process-of-changing-over-to-straightel)
    - [Step 1. Bootstrap `straight.el`](#step-1-bootstrap-straightel)
    - [Step 2. Convert/Remove `package.el` stuff](#step-2-convertremove-packageel-stuff)
        - [Delete the `package.el` initialization](#delete-the-packageel-initialization)
        - [Remove `:ensure` from `use-package`](#remove-ensure-from-use-package)
        - [Remove `defer` from `use-package`](#remove-defer-from-use-package)
        - [Get rid of `auto-package-update` package](#get-rid-of-auto-package-update-package)
        - [Put in place `org` workaround](#put-in-place-org-workaround)
- [Conclusions?](#conclusions)

<!-- markdown-toc end -->


## Why switch?

I've been using `package.el` since emacs25. The `use-package` notation came as part of the init files I've been using for _YEARS_ from the [Emacs Bootstrap](http://emacs-bootstrap.com/#first) website.

However, there were a couple of annoyances with `package.el`, the top one being the ``custom-set-variables` `package-selected-packages`` that would change each time packages were installed / reinstalled, and then again when you loaded the package list (which writes this variable to disk). And it's in "alphabetical order" except that newly installed packages are placed at the head of the list. But then, when you restart emacs and loaded the package list, the whole list would be re-alphabetized again.

This was annoying for two reasons:

1. The canonical package list was not maintained directly in user-specified files (i.e., my startup files), but indirectly in this variable maintained by emacs `package.el` housekeeping.
2. I sync my emacs startup files across multiple machines and platforms via a Git repo of my home directory dotfiles. The multiple iterations of removing or re/installing and synchronizing this package list on _each_ platform and machine were updated was time-consuming busywork and imperfect at best.

[`straight.el`](https://github.com/raxod502/straight.el "straight.el GitHub Repo") solves the problem of maintaining package list directly in startup files, which solves both of those issues. Furthermore,** seamless integrating git repositories of emacs packages**, which can be locally edited, and even pointing to forked repos, is a strong appeal of `straight.el`, when I am getting to the point of being comfortable reading and understanding Emacs Lisp in the package repositories.

## The process of changing over to `straight.el`

There are two main steps to switch to `straight.el`:
1. Bootstrap the `straight.el` install code snippet into your `init.el`
2. Convert and remove `package.el` things that are incompatible with `straight.el`

This post will not even delve into pointing to custom repos; see the `straight.el` documentation for those details.

### Step 1. Bootstrap `straight.el`

Using the ["Getting started" in README.md](https://github.com/raxod502/straight.el/blob/develop/README.md#getting-started) as definitive guide, put the following code snippet into your Emacs `init.el`:

```emacs-lisp
(defvar bootstrap-version)
(let ((bootstrap-file
       (expand-file-name "straight/repos/straight.el/bootstrap.el" user-emacs-directory))
      (bootstrap-version 5))
  (unless (file-exists-p bootstrap-file)
    (with-current-buffer
        (url-retrieve-synchronously
         "https://raw.githubusercontent.com/raxod502/straight.el/develop/install.el"
         'silent 'inhibit-cookies)
      (goto-char (point-max))
      (eval-print-last-sexp)))
  (load bootstrap-file nil 'nomessage))
```

That's it! And including this configuration here, since `straight.el` has this nice property of being "backward compatible" with `package.el`-- all my current packages and settings were available directly via `straight.el` by [activating this functionality](https://github.com/raxod502/straight.el/blob/develop/README.md#integration-with-use-package) per:

```emacs-lisp
;;;;  Effectively replace use-package with straight-use-package
;;; https://github.com/raxod502/straight.el/blob/develop/README.md#integration-with-use-package
(straight-use-package 'use-package)
(setq straight-use-package-by-default t)
```

Again, that is placed in your `init.el` after `straight.el` is bootstrapped. It effectively makes `use-package` call sites in your startup files become `straight-use-package`.

### Step 2. Convert/Remove `package.el` stuff

From the `README.md` :

> You should remove any code that relates to `package.el`; for example,
> references to `package-initialize`, `package-archives`, and (if you're
> using [`use-package`](#) `:ensure` or `use-package-always-ensure`.
> While it is technically possible to use
> both `package.el` and `straight.el` at the same time, there is no real
> reason to, and it might result in oddities like packages getting
> loaded more than once.

Below are the steps I took and representative edits I made to get my startup files switched over. Once the two main steps have been completed, (1. bootstrap and 2. `package.el` removal parts) restart your Emacs session.

`straight.el` will happily clone all the package repositories referenced in your startup files, including any dependencies, and put those clone checkouts within `<user-emacs-directory>/striaght/`. And it all just works, on both macOS and Ubuntu Linux. The first time takes a little longer to do all the network retrievals, of course...

#### Delete the `package.el` initialization

All the following had to go. It was **DELETED**:

```emacs-lisp
;;______________________________________________________________________
;;;;  package management related

(require 'package)

;;
(add-to-list 'package-archives
                '("melpa" . "https://melpa.org/packages/"))

;; for latest org-mode and org-plus-contrib
(add-to-list 'package-archives '("org" . "https://orgmode.org/elpa/") t)

;; https://github.com/purcell/emacs.d/blob/master/lisp/init-elpa.el#L64
;; (setq package-enable-at-startup nil)
(package-initialize)

(when (not package-archive-contents)
  (package-refresh-contents))

(unless (package-installed-p 'use-package)
  (package-install 'use-package))

;; install packages automatically if not already present on your
;; system to be global for all packages
(require 'use-package-ensure)
(setq use-package-always-ensure t)
```

BUT WAIT... I still wanted to use MELPA and `M-x package-list-packages` to peruse the MELPA repos... So I ended up with the following minimal `package.el` config, placed _after_ the `straight.el` bootstrap and config:

```emacs-lisp
;;;;  package.el
;;; so package-list-packages includes them
(require 'package)
(add-to-list 'package-archives
             '("melpa" . "https://melpa.org/packages/"))
```

This doesn't harm the `straight.el` installation, so for me it's the best of both worlds.

#### Remove `:ensure` from `use-package`

I had numerous `:ensure t` sprinkled through my startup files. And I sometimes had `:ensure <pkgname>` or a specific load ordering placed in the file.

There is no need for `:ensure t`
```diff
 (use-package web-mode
-  :ensure t
   :after flycheck
   :bind (("C-c ]" . emmet-next-edit-point)
          ("C-c [" . emmet-prev-edit-point)
```

 If there was a true dependency, I switched to `:requires` from `use-package`, as it probably should have been handled that way anyway:

```diff
 (use-package ivy-rich
+  :requires (counsel)
   :config
   (setq
    ivy-rich-path-style 'abbrev
```

```diff
 ;; https://github.com/raxod502/prescient.el
 (use-package company-prescient
+  :requires (prescient)
   :config
   (company-prescient-mode 1)
   (prescient-persist-mode 1)
```

#### Remove `defer` from `use-package`

Not strictly necessary, but startup speeds with `straight.el` seem to have improved over `package.el` so I ripped them out:

```diff
 ;; https://github.com/ardumont/markdown-toc
 ;; M-x markdown-toc-generate-or-refresh-toc
-(use-package markdown-toc
-  :defer 2)
+(use-package markdown-toc)
```

#### Get rid of `auto-package-update` package

```diff
-;; keep packages updated automatically
-;; https://github.com/rranelli/auto-package-update.el
-(use-package auto-package-update
-  :init
-  (setq auto-package-update-last-update-day-filename (expand-file-name "last-package-update-day" temp-dir))
-  :config
-  (setq auto-package-update-delete-old-versions t)
-  (auto-package-update-at-time "23:00")
-  ;; (setq auto-package-update-hide-results t)
-  ;; (setq auto-package-update-prompt-before-update t)
-  (auto-package-update-maybe))
-
```

`straight.el` has a bound method to sync all your locally specified package clones: `straight-normalize-all`

It can be executed directly
```
 M-x straight-normalize-all
```

Refer to the docs at [Automatic repository managment](https://github.com/raxod502/straight.el#automatic-repository-management) for more details.

#### Put in place `org` workaround

Straight from the `README`: [Installing Org with `straight.el`](https://github.com/raxod502/straight.el/blob/develop/README.md#installing-org-with-straightel)

```diff
-(use-package org
+
+;;______________________________________________________________________
+;;;;  Installing Org with straight.el
+;;; https://github.com/raxod502/straight.el/blob/develop/README.md#installing-org-with-straightel
+(require 'subr-x)
+(straight-use-package 'git)
+
+(defun org-git-version ()
+  "The Git version of 'org-mode'.
+Inserted by installing 'org-mode' or when a release is made."
+  (require 'git)
+  (let ((git-repo (expand-file-name
+                   "straight/repos/org/" user-emacs-directory)))
+    (string-trim
+     (git-run "describe"
+              "--match=release\*"
+              "--abbrev=6"
+              "HEAD"))))
+
+(defun org-release ()
+  "The release version of 'org-mode'.
+Inserted by installing 'org-mode' or when a release is made."
+  (require 'git)
+  (let ((git-repo (expand-file-name
+                   "straight/repos/org/" user-emacs-directory)))
+    (string-trim
+     (string-remove-prefix
+      "release_"
+      (git-run "describe"
+               "--match=release\*"
+               "--abbrev=0"
+               "HEAD")))))
+
+(provide 'org-version)
+
+;; (straight-use-package 'org) ; or org-plus-contrib if desired
+
+(use-package org-plus-contrib
   :mode (("\\.org$" . org-mode))
-  :ensure org-plus-contrib
   :bind
   ("C-c l" . org-store-link)
   ("C-c a" . org-agenda)
```

Note I can use `(use-package org-plus-contrib ...` instead of `(straight-use-package org-plus-contrib ...` since I've already configured it to behave that way (see above).

## Conclusions?

I didn't know how difficult versus easy this was going to be before I started. Because of the nice "compatibility" features `straight.el` has, it turned out to be rather trivially simple in my case... So if there's editing emacs packages in your future, or some of the annoyances of `package.el` have gotten to you, I'd recommend you take a look at `straight.el` to replace `package.el`.
