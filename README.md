# sealsay

```bash
     ------
    <  yo  >
     ------
       \
        \                             ---\/---
         \      ------                \  || /
          \    .  .  /\ -----------\   \   /
           \  *     /               \  /  /
            - (--)                   \/  /
               \      | \               /
                -------\ \-------------/
                        \ |
```

A seal that lives in your terminal. Inspired by cowsay!

## Install

**Requires Python3**

Install python from the [official website](https://www.python.org/downloads/)

OR

```bash
# apt (Debian / Ubuntu)
$ sudo apt install python

# pacman (Arch)
$ pacman -S python3

# Homebrew (Linux / MacOS)
$ brew install python
```

### AUR (Arch Linux)

```bash
yay -S sealsay
```

### Manual

1: Clone the repo:

```bash
$ git clone https://github.com/phantypengy/sealsay
$ cd sealsay
```

2: Make script executable & add it to PATH:

```bash
$ chmod +x sealsay

# Linux / macOS:
$ sudo mv sealsay /usr/local/bin/sealsay

# Windows (MSYS2):
$ mv sealsay /usr/bin/sealsay
# Note that this program will only work through the MSYS2 terminal
```

After running the mv command, it is safe to delete the remains of the repo

## Usage

Same format as cowsay, for example:

```bash
sealsay -s hello world
```

There are currently 3 different seals that can be used via "-":
-s : basic seal

-t : tired seal

-l : sea lion

Seals are stored in /usr/share/sealsay/seals/ as .txt files.
