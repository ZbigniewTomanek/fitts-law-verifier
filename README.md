# fitts-law-verifier
Simple tool that's allows you to verify fitts law (https://en.wikipedia.org/wiki/Fitts%27s_law)

## Overview ##

This simple tool allows you to verify your fitts' rights yourself. It works by clicking the buttons that appear and analyzing the data generated in this way.

## Installation ##

Python 3.6 is necessary to run this app. You can download it from [here](https://www.python.org/downloads/release/python-3612/).
Becauese of kivy library it's not compatible with python 3.8 yet.

You can clone and run the app with following commands:
```
git clone https://github.com/ZbigniewTomanek/fitts-law-verifier.git
cd fitts-law-verifier
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## Usage ##

After running program the `spacebar` will spawn new button. After button spawn you have to click it as fast as you can.
You can manually change values of Fitts law constants `a`, `b` and `c` in `def add_fitts_data_to_df`. The default ones seems to be working on my machine.


### Modes ###

`Size mode` means that the buttons will be spawned in similiar distance, but different sizes.
Similarly in `distance mode`, buttons size will be the same, however the spawn distances from cursor will vary. 

### Buttons ###
After picking up enough samples you can save data to `fitts.csv` and show plot with `escape` button.

Clicking button `e` will generate the plot, save data and delete all current samples.
