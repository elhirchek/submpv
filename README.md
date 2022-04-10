# Submpv



## Overview 

**submpv** is a python script to automate downloading and adding subtitle from subscence

## Download Prosses

```bash
git clone https://github.com/yassin-l/submpv.git
cd submpv
pip install -r requirements.txt
mv submpv.lua $HOME/.config/mpv/scripts
# and change path to the script submpv.py
# by default key to run submpv is g (you can change it by editing submpv.lua)
```

### Note

you can use submpv.py as sperated script to download subtitle from subscence

### Usage of submpv.py

```bash
python3 submpv.lua "Tv.show.name.S01E07" # this example is the best way to get good resault, with "." rather then spaces
```

## Todo List

- [ ] add support for movies
