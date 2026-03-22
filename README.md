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

A seal that lives in your terminal, for Linux and macOS. Inspired by cowsay!

## Requirements

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

## Install

### AUR (Arch Linux)

```bash
yay -S sealsay
```

### Homebrew (macOS)

```bash
brew tap phantypengy/sealsay https://github.com/phantypengy/sealsay
brew install sealsay
```

### Manual

1: Clone the repo:

```bash
git clone https://github.com/phantypengy/sealsay
cd sealsay
```

2: Make script executable & add it to PATH:

```bash
chmod +x sealsay

# Linux / macOS:
sudo mv sealsay /usr/local/bin/sealsay
```

After running the mv command, it is safe to delete the remains of the repo

## Usage

Same format as cowsay:

```bash
sealsay seals are the best!


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
