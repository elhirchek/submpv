# Submpv

# Note

This project is no longer supported nor working due to Subscene being closed.

## Overview 

**submpv** is a python script to automate downloading and loading subtitle from subscence.

## Dependencies

This lua script depend on python3 been already installed.

```bash
# for windows go to the official python website.
apt install python3 -y
```

## Setup

### Windows

Install the zip file from github and extract the folder in **[Drive]:\Users\\[User]\AppData\Roaming\mpv\scripts\\**.

```bash
# to get python path run the following command:
where python
# open cmd in the directory of this script and run:
pip install -r requirements.txt
```

### Linux
```bash
git clone https://github.com/yassin-l/submpv.git
mv ./submpv ~/.config/mpv/scripts/
cd ~/.config/mpv/scripts/submpv
pip install -r requirements.txt
```

### Note

> change the /bin/python path inside [[]] in the main.lua file to your python path.

> add this line to your input.conf **[key] script-binding "submpv"**, where key is your key.

> you can use submpv.py as sperated script to download subtitle from subscence.

### Usage of submpv.py

```bash
python3 submpv.lua "Tv.show.name.S01E07"
```

## Todo List
- [x] support for movies
- [ ] renaming subtitle as the target name ( by [ayghub](https://github.com/ayghub/) ).
- [ ] config file
