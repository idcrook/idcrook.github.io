---
layout: post
title: My Emacs Rust Language Config
date: 2020-03-25
mathjax: False
comments: True
image: /images/emacs-rust-in-use.png
---

I recently bought a [Kindle version](https://www.amazon.com/dp/B071YKRV8Q/) of the [Rust book](https://doc.rust-lang.org/book/), and worked [my way through it](https://github.com/idcrook/burst). Emacs has good support available for cargo and rust.

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->

- [Why Rust?](#why-rust)
- [rust and cargo](#rust-and-cargo)
    - [Full .emacs.d for Rust](#full-emacsd-for-rust)

<!-- markdown-toc end -->


## Why Rust?

As I mentioned in a [previous post](https://idcrook.github.io/raytracing-iow-in-cpp-cuda-and-optix/#building), the last time I used C++ for a project before this year was over twenty years ago. C++ has evolved, attempting to address some weaknesses and relative advantages or disadvantages in that time. I'm not going to cover what these are here, but will say that Rust seems to fill similar roles as C++ but starting from a code security point-of-view.

I was learning swiftlang in the Swift 2/3 era, and after my recent introduction to Rust, I often found myself saying "Oh, this must is where Swift got this idiom from". In a weird way from a simple "writing code" viewpoint, I feel like Rust is in-between Javascript and C++. Kinda like Swift. Where the compiler and borrow checker are always right there letting you know things you need to flesh out in your code.

## rust and cargo

I have been using an Ubuntu Linux machine to learn Rust. I have [decided to use](https://github.com/idcrook/burst/blob/main/notes/emacs.org) with the web+sh [rustup installer](https://rustup.rs/). It has been and incorporated into my dotfiles.


```shell
❯ curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

This has worked on Ubuntu Linux, a Raspberry Pi running Raspbian buster, and macOS Catalina.

[Cargo](https://doc.rust-lang.org/cargo) is the Rust *package manager* and is included in its install. It is wonderful, handling library dependencies, builds, testing, crates.io  and more.

For the emacs side of things, I started with the Rust section on [http://emacs-bootstrap.com/](http://emacs-bootstrap.com/) and have arrived at a modified version of that. A list of emacs packages (from my [lang-rust.el](https://github.com/idcrook/.emacs.d/blob/main/elisp/lang-rust.el) file):

 - rust-mode
 - flycheck-rust
 - cargo - run cargo commands for crates from within emacs
 - racer

[Racer](https://github.com/racer-rust/emacs-racer) warrants further mention as it pulls in IDE-like features for rust dev right in emacs. Racer is written in rust, and I installed it using-- you guessed it-- rustup and cargo, as described on its webpage.


```shell
# https://github.com/racer-rust/emacs-racer#installation
rustup toolchain add nightly
rustup component add rust-src
cargo +nightly install racer
```

![lookup library function in rust in emacs](/images/emacs-rust-in-use.png)


### Full .emacs.d for Rust

Some comments and details elided, Full file here:  [lang-rust.el](https://github.com/idcrook/.emacs.d/blob/main/elisp/lang-rust.el)

```lisp
;; started from http://emacs-bootstrap.com/

;; rust-mode
;; https://github.com/rust-lang/rust-mode
(use-package rust-mode
  :bind ( :map rust-mode-map
               (("C-c C-t" . racer-describe)
                ([?\t] .  company-indent-or-complete-common)))
  :config
  (progn
    ;; add flycheck support for rust (reads in cargo stuff)
    ;; https://github.com/flycheck/flycheck-rust
    (use-package flycheck-rust)

    ;; cargo-mode for all the cargo related operations
    ;; https://github.com/kwrooijen/cargo.el
    (use-package cargo
      :hook (rust-mode . cargo-minor-mode)
      :bind
      ("C-c C-c C-n" . cargo-process-new)) ;; global binding

    ;;; separedit ;; via https://github.com/twlz0ne/separedit.el
    (use-package separedit
      :straight (separedit :type git :host github :repo "idcrook/separedit.el")
      :config
      (progn
        (define-key prog-mode-map (kbd "C-c '") #'separedit)
        (setq separedit-default-mode 'markdown-mode)))


    ;;; racer-mode for getting IDE like features for rust-mode
    ;; https://github.com/racer-rust/emacs-racer
    (use-package racer
      :hook (rust-mode . racer-mode)
      :config
      (progn
        ;; package does this by default ;; set racer rust source path environment variable
        ;; (setq racer-rust-src-path (getenv "RUST_SRC_PATH"))
        (defun my-racer-mode-hook ()
          (set (make-local-variable 'company-backends)
               '((company-capf company-files)))
          (setq company-minimum-prefix-length 1)
          (setq indent-tabs-mode nil))

        (add-hook 'racer-mode-hook 'my-racer-mode-hook)

        ;; enable company and eldoc minor modes in rust-mode (racer-mode)
        (add-hook 'racer-mode-hook #'company-mode)
        (add-hook 'racer-mode-hook #'eldoc-mode)))

    (add-hook 'rust-mode-hook 'flycheck-mode)
    (add-hook 'flycheck-mode-hook 'flycheck-rust-setup)

    ;; format rust buffers on save using rustfmt
    (add-hook 'before-save-hook
              (lambda ()
                (when (eq major-mode 'rust-mode)
                  (rust-format-buffer))))))

```
