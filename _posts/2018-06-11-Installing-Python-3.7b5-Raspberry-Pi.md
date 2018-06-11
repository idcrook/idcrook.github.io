---
layout: post
comments: false
title: Compiling and Installing Python 3.7 b5 on Raspberry Pi
date: 2018-06-11
---

Python3.7 is [scheduled](https://www.python.org/dev/peps/pep-0537/#schedule) to be released at the end of June 2018. I wanted to explore some of the [new things](https://docs.python.org/3.7/whatsnew/3.7.html) and put it on a Raspberry PI. Here are the instructions.

# Building python 3.7 beta on Raspberry Pi

based on steps found at [https://www.scivision.co/compile-install-python-beta-raspberry-pi/](https://www.scivision.co/compile-install-python-beta-raspberry-pi/)

## my steps

Choose a Pi
```bash
# Pi 3 B+
ssh rpihp1
screen -R
```

```shell
$ df -h .
Filesystem      Size  Used Avail Use% Mounted on
/dev/root        59G  1.2G   55G   3% /
```
plenty of disk space. (after python3.7b5 install, I had about 400MB less disk space)

Install some pre-reqs
```bash
sudo apt install -y libffi-dev libbz2-dev liblzma-dev \
    libsqlite3-dev libncurses5-dev libgdbm-dev zlib1g-dev \
    libreadline-dev libssl-dev tk-dev build-essential \
    libncursesw5-dev libc6-dev openssl git
```

We are going to build from Python [source code](https://github.com/python/cpython/releases).

Download, extract, configure, compile and install
```bash
mkdir -p ~/projects/python37
wget https://github.com/python/cpython/archive/v3.7.0b5.tar.gz
tar zxvf v3.7.0b5.tar.gz
cd cpython-3.7.0b5
./configure --prefix=$HOME/.local --enable-optimizations

make -j 5 -l 4  # quad core, so set j=4+1
make install
```
Note: It's kinda fun to watch `htop` updated when the compilation is running...

Once installed, setup environment in your `~/.profile` to add the new home of python3.7 to your path:
```bash
# set PATH so it includes user's private ~/.local/bin if it exists
if [ -d "$HOME/.local/bin" ] ; then
	PATH="$HOME/.local/bin:$PATH"
fi
```

log out of all shells to get this new setting

## Running

Tkinter is included...
```python
pi@rpihp1:~ $ python3.7
Python 3.7.0b5 (default, Jun 10 2018, 16:24:31)
[GCC 6.3.0 20170516] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from tkinter import *
>>> ^D
```

The New-in-3.7 `@dataclass` decorator is available
```python
>>> from dataclasses import dataclass
>>> @dataclass
... class SimpleDataObject(object):
...   '''
...   In this case,
...   __init__, __repr__, __eq__,  will all be generated automatically.
...   '''
...
...   field_a: int
...   field_b: str
...
>>> example = SimpleDataObject(1, 'b')
>>> print(example)  # SimpleDataObject(field_a=1, field_b='b')
SimpleDataObject(field_a=1, field_b='b')
>>>
```
