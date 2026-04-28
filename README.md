# sealsay

![AUR version](https://img.shields.io/aur/version/sealsay)

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

## Dependencies

**Requires Python3**

Install python from the [official website](https://www.python.org/downloads/)

OR

```bash
# apt (Debian / Ubuntu)
sudo apt install python

# pacman (Arch)
pacman -S python3

# Homebrew (Linux / MacOS)
brew install python
```

## Package managers

### AUR (Arch Linux)

```bash
yay -S sealsay
```

## Manual install

1: Clone the repo:

```bash
git clone https://github.com/phantypengy/sealsay
cd sealsay
```

2: Install with pip:

```bash
python3 -m pip install .
```

3: Run it:

```bash
sealsay -s "hello"
```

## Usage

sealsay [-modifier] [message]

```bash
$ sealsay -s seals are the best!


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

## Possible modifiers:

### Seal variants:

<!-- SEALS:START -->
-b: basic seal

-o: old seal

-t: triple seal

<!-- SEALS:END -->

_-t and -o were taken from ASCII.co.uk_

### Other commands:

-h: help (shows usage)

## Star History

<a href="https://www.star-history.com/?repos=phantypengy%2Fsealsay&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=phantypengy/sealsay&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=phantypengy/sealsay&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=phantypengy/sealsay&type=date&legend=top-left" />
 </picture>
</a>
