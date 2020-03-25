---
layout: post
title: Emacs and C++ and CUDA
date: 2020-03-24
mathjax: False
comments: True
image: /images/emacs-editing-optix-cuda-header.png
---

Recently, I got an Nvidia GeForce (RTX series) card. I've been using it to learn about graphics programming and raytracing and things like that under Linux. And I am using Emacs to editing the C++ files that all the graphics SDKs seem to use.

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->

- [Using CUDA](#using-cuda)
- [Using emacs with CUDA files](#using-emacs-with-cuda-files)
- [Configure emacs for CUDA code](#configure-emacs-for-cuda-code)
    - [Install Irony server](#install-irony-server)
    - [cuda-mode](#cuda-mode)
    - [Notes on Cmake](#notes-on-cmake)
    - [See my .emacs.d for more](#see-my-emacsd-for-more)

<!-- markdown-toc end -->

## Using CUDA

There is a C/C++-based programming framework called CUDA (stands for "Compute Unified Device Architecture") that Nvidia created some time ago for GPGPU programming. In some cases it has been exapnded from that role, and OptiX shader code can be written in it. OptiX is another Nvidia SDK, this one for raytracing applications.

What has became convenient lately is that Ubuntu (my distro of choice for desktop Linux) has made a package available to install the CUDA SDK. So on Ubuntu 19.10, and the soon-to-be released Ubuntu 20.04, you can get a usable CUDA SDK install "out of the box".


```shell
sudo apt install nvidia-cuda-toolkit
```

**NOTE**: Other related SDKs may require you to be a registered developer with Nvidia in order to download and install them.

The CUDA toolkit comes with `nvcc - The NVIDIA CUDA Compiler` and it even allows _builds_  on a host that doesn't have an Nvidia graphics card installed.  Of course, something linked against the CUDA runtime on a system that doesn't have the underlying Nvidia hardware/driver won't run.


![Emacs in a .cuh file CUDA header](/images/emacs-editing-optix-cuda-header.png)


## Using emacs with CUDA files

There are some established naming conventions for CUDA format files using file extensions.

- Cuda source code files: "`.cu`",
- Cuda source headers: "`.h`", "`.cuh`"

Flycheck is "[On the fly syntax checking for GNU Emacs](https://github.com/flycheck/flycheck)", and it includes built-in support for CUDA files.  Since `nvcc` is the compiler, `flycheck` uses it to check `cuda-mode` files. `nvcc` uses file extensions to determine type of file and type of processing to do on it, but does not specifically recognize "`.cuh`" extensions. So even if Emacs knew if was a CUDA-mode file, flycheck would not work, because `nvcc` would not work.

I was able to send a [PR to flycheck](https://github.com/flycheck/flycheck/pull/1699) project to fix this, [[cuda-nvcc: Does not work with .h or .cuh files]](https://github.com/flycheck/flycheck/issues/1673). Now any CUDA source header files will also work with flycheck.


## Configure emacs for CUDA code

### Install Irony server

I was able to use [`irony-mode`](https://github.com/Sarcasm/irony-mode) and its kin for the C++-side handling in emacs.

On ubuntu, this means installing some pre-reqs to be able to build the irony-server.

```shell
sudo apt install cmake libclang1 libclang-dev
```

If those pre-reqs are met, then within Emacs with the `irony` package installed, the emacs package itself can down, build, and install the irony server for its use. <kbd>M-x irony-install-server</kbd>

See [elisp/lang-cpp.el](https://github.com/idcrook/.emacs.d/blob/95a38d3f34afd51579537642beb190351ee7a183/elisp/lang-cpp.el#L40) in my shared `.emacs.d` repo for additional details.

### cuda-mode


```lisp
;;; https://github.com/chachi/cuda-mode
(use-package cuda-mode)

;; add path manually;
(add-hook 'cuda-mode-hook
          (lambda ()
            ( setq c-basic-offset              4
                   flycheck-cuda-include-path (list "."))
            ))

;; later, after irony is loaded
(push 'cuda-mode irony-supported-major-modes)

```


### Notes on Cmake

CMake is a tool to facilitate more robust cross-platform C++ builds and is popular for the C++ projects that seem to dominate in the computer graphics world.

There is a way to have CMake generate a file that other tools can use to determine proper compile commands and include directories and the like.

```shell
# example command that will also creates compile_commands.json
cmake -D CMAKE_EXPORT_COMPILE_COMMANDS=ON  -B build .
```

So, some other related emacs packages and config for cmake. the `irony-cdb-autosetup-compile-options` is how to tell irony to automatically look for the `compile_commands.json` files


```lisp
;;; https://github.com/Lindydancer/cmake-font-lock
(use-package cmake-font-lock)

;; use compile_commands.json obtained from CMake -D CMAKE_EXPORT_COMPILE_COMMANDS=O
(add-hook 'irony-mode-hook 'irony-cdb-autosetup-compile-options)
```

## See my .emacs.d for more

I have finally made it possible to share my .emacs.d, available in a GitHub repo [idcrook/.emacs.d](https://github.com/idcrook/.emacs.d)

The C++ file .emacs.d init file is found at [lang-cpp.el](https://github.com/idcrook/.emacs.d/blob/master/elisp/lang-cpp.el)

It is also included as part of my dotfiles repo, [i-dotfiles](https://github.com/idcrook/i-dotfiles) (as a git submodule)
