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

2: Make script executable & add it to PATH:

```bash
chmod +x sealsay

# Linux / macOS:
sudo mv sealsay /usr/local/bin/sealsay
```

3: Move seals/ directory to /usr/share:

```bash
# Linux
mv seals/ /usr/share/seals/

# macOS
mv seals/ /usr/local/share/seals/
```

After running the mv command, it is safe to delete the remains of the repo

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

-s: original seal

-t: triple seal

-o: basic seal

*-t and -o were taken from ASCII.co.uk* 

### Other commands:

-h: help (shows usage)
