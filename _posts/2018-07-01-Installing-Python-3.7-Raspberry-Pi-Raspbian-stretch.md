---
layout: post
mathjax: false
comments: false
title: Compiling and Installing Python 3.7 on Raspberry Pi Running Raspbian Stretch
date: 2018-07-01
image: /images/raspi-python3p7-final-repl.png
---

Python3.7 final has been [released](https://www.python.org/dev/peps/pep-0537/#schedule) near end of June 2018. Here are the instructions on how to build from source on a Raspberry Pi running Raspbian `stretch`.

# Building Python 3.7 on Raspberry Pi

## my steps

Choose a Raspberry Pi and `ssh` to it.

```bash
# Pi 3 B+
ssh rpihp1
screen -D -R
df -h .
```

A full build, test and install flow will consume about 400MB of disk space.

We are going to build from Python [source code](https://github.com/python/cpython/releases).

First, install some pre-reqs for the build:

```bash
sudo apt install -y libffi-dev libbz2-dev liblzma-dev \
    libsqlite3-dev libncurses5-dev libgdbm-dev zlib1g-dev \
    libreadline-dev libssl-dev tk-dev build-essential \
    libncursesw5-dev libc6-dev openssl git
```


**Download, extract, configure, compile and install** from the source code.

Note: It's kinda fun to watch `htop` updated when the compilation is running...

```bash
C-a c
sudo apt-get install -y htop
sudo htop
C-a C-a
```

<kbd>C-a c</kbd>
Means hold down <kbd>Control</kbd> key and type letter <kbd>a</kbd>, then release <kbd>Control</kbd> key add type letter <kbd>c</kbd>

<kbd>C-a C-a</kbd>
Means hold down <kbd>Control</kbd> key and type letter <kbd>a</kbd>, then keep <kbd>Control</kbd> presses and type another letter <kbd>a</kbd>


In a `screen` session:
<kbd>C-a c</kbd> :: will "**c**"reate another `screen` window.
<kbd>C-a C-a</kbd> :: will alternate switching between last two accessed windows in `screen` session.
<kbd>C-a d</kbd> :: will "**d**"etach from `screen` session, dropping you back to the screen you launched it from.
Finally
`screen -D -R` will reconnect to running `screen` session

OK. Enough with the GNU Screen short lesson. **Let's do it**:

```bash
mkdir -p ~/projects/python37
cd ~/projects/python37
wget https://github.com/python/cpython/archive/v3.7.0.tar.gz
tar zxvf v3.7.0.tar.gz
cd cpython-3.7.0
./configure --prefix=$HOME/.local --enable-optimizations

# Throttle parallel make so that load average ('-l') stays under 4
make -j 4 -l 4  # quad core, so setting j=4+1 ('-j 5') also seemed fine
# ... This takes a while. Compiles, runs test and profiles ...
make install
```

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
Python 3.7.0 (default, Jul  1 2018, 01:16:29)
[GCC 6.3.0 20170516] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from tkinter import *
>>> dir()
['ACTIVE', 'ALL', 'ANCHOR', 'ARC', 'BASELINE', 'BEVEL', 'BOTH', 'BOTTOM', 'BROWSE', 'BUTT', 'BaseWidget', 'BitmapImage', 'BooleanVar', 'Button', 'CASCADE', 'CENTER', 'CHAR', 'CHECKBUTTON', 'CHORD', 'COMMAND', 'CURRENT', 'CallWrapper', 'Canvas', 'Checkbutton', 'DISABLED', 'DOTBOX', 'DoubleVar', 'E', 'END', 'EW', 'EXCEPTION', 'EXTENDED', 'Entry', 'Event', 'EventType', 'FALSE', 'FIRST', 'FLAT', 'Frame', 'GROOVE', 'Grid', 'HIDDEN', 'HORIZONTAL', 'INSERT', 'INSIDE', 'Image', 'IntVar', 'LAST', 'LEFT', 'Label', 'LabelFrame', 'Listbox', 'MITER', 'MOVETO', 'MULTIPLE', 'Menu', 'Menubutton', 'Message', 'Misc', 'N', 'NE', 'NO', 'NONE', 'NORMAL', 'NS', 'NSEW', 'NUMERIC', 'NW', 'NoDefaultRoot', 'OFF', 'ON', 'OUTSIDE', 'OptionMenu', 'PAGES', 'PIESLICE', 'PROJECTING', 'Pack', 'PanedWindow', 'PhotoImage', 'Place', 'RADIOBUTTON', 'RAISED', 'READABLE', 'RIDGE', 'RIGHT', 'ROUND', 'Radiobutton', 'S', 'SCROLL', 'SE', 'SEL', 'SEL_FIRST', 'SEL_LAST', 'SEPARATOR', 'SINGLE', 'SOLID', 'SUNKEN', 'SW', 'Scale', 'Scrollbar', 'Spinbox', 'StringVar', 'TOP', 'TRUE', 'Tcl', 'TclError', 'TclVersion', 'Text', 'Tk', 'TkVersion', 'Toplevel', 'UNDERLINE', 'UNITS', 'VERTICAL', 'Variable', 'W', 'WORD', 'WRITABLE', 'Widget', 'Wm', 'X', 'XView', 'Y', 'YES', 'YView', '__annotations__', '__builtins__', '__doc__', '__loader__', '__name__', '__package__', '__spec__', 'constants', 'enum', 'getboolean', 'getdouble', 'getint', 'image_names', 'image_types', 'mainloop', 're', 'sys', 'wantobjects']
>>>
```

The [New-in-3.7 `@dataclass` decorator](https://www.python.org/dev/peps/pep-0557/) is available
```python
>>> from dataclasses import dataclass
>>> @dataclass
... class SimpleDataObject(object):
...   field_a: int
...   field_b: str
...
>>> example = SimpleDataObject(1, 'b')
>>> print(example)  # SimpleDataObject(field_a=1, field_b='b')
SimpleDataObject(field_a=1, field_b='b')
>>>
```
