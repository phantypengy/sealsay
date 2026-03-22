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

Same format as cowsay:

```bash
$ sealsay seals are the best!


     -----------------------
    <  seals are the best!  >
     -----------------------
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
