# potato-timer
A simple Pomodoro-style timer with intuitive CLI, written in Python. Developed and tested
in Pop!_OS Linux and occasionally tested in Windows 10.

![Potato Timer UI in color](assets/potato-timer_ui.png)

## Downloading the timer
Easiest way to get the program is to install via `pip`:
```
pip install potatotimer
```
and create your own config.yml file. More info on configuration [down below](#configuration). 

## Running from source

### Getting the source code files
Clone this repository to the folder of your choice:
```
git clone https://github.com/mtijas/potato-timer.git
```

### Dependencies
Potato Timer uses python to run so it should obviously be installed.
Minimum required version of python is 3.7.

PyYAML package is used to read settings files. Install the package with pip:
```
pip install pyyaml
```

Appdirs is used to help find the preferred config location. Install with pip:
```
pip install appdirs
```

Curses is used to draw the user interface. In Linux it might already be installed 
but in Windows you should install the `windows-curses` PyPI package:
```
pip install windows-curses
```

### Starting the program
Since there is no compiled binaries available the program should be started with python:
```
python scripts/potatotimer
```

## Configuration
Timers can be configured using YAML. You should create one of those 
configuration files listed below, or you may provide an alternative  
configuration file with the command line option `-c 'path/to/config.yml'`.

Config will be automatically searched from (in this order):
- config file provided via command line option
- `$XDG_CONFIG_HOME/potatotimer/config.yml`
- `~/.config/potatotimer/config.yml`
- `~/.potatotimer-config.yml`

[An example configuration file](#example-configuration-file) is something worth looking at.

More on [$XDG_CONFIG_HOME](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html).

### Timers
Timers are configured as a list of type-duration pairs, where type is basically 
the name of the timer and duration is given in minutes. Built-in types of timers 
are `work`, `short break` and `long break`, though you may call your timers whatever 
you like `i.e. coffee break`.

A single work timer would be configured as follows:
```yaml
timers:
  - type: "work"
    duration: 25
```

Decimals are also accepted for duration (i.e. `duration: 0.1` is a timer lasting 6 seconds).
More thorough example of timer configuration can be found 
[in the example configuration file](#example-configuration-file).

### Alarm type
Alarm type can be either `beep` or `flash`. 

- `beep` rings the terminal bell
- `flash` flashes the terminal window.

The default when setting omitted from the file is `beep`.

Example: `alarm_type: "beep"`

### Alarm repeat
Number of times alarm will sound/flash each time alarm triggers.

Example: `alarm_repeat: 3`

### Use of colors
When `use_colors` is se to `True` the program will be beautifully decorated with 
meaningful colors for different types of timers:

- `work` is red
- `short break` is green
- `long break` is blue
- Any other type of timer will be yellow. 

Set this `False` and the program will be plain black and white. The default is `True`.

If you prefer to use the colors from your terminal, set `prefer_terminal_colors`
to `True`. For both the terminal and built-in color schemes the background will be "transparent", 
as in not have any other color than what your terminal has.

### Example configuration file

```yaml
alarm_type: "beep"
alarm_repeat: 2
use_colors: True
prefer_terminal_colors: False
timers:
  - type: "work"
    duration: 25
  - type: "short break"
    duration: 5
  - type: "work"
    duration: 25
  - type: "short break"
    duration: 5
  - type: "work"
    duration: 25
  - type: "short break"
    duration: 5
  - type: "work"
    duration: 25
  - type: "long break"
    duration: 35

```

More sample configs in the [sample-configs folder](sample-configs/).