# tomato-timer
A simple Pomodoro-style timer with intuitive CLI, written in Python. Developed and tested
in Pop!_OS Linux so the program might not work in any other OS than Debian-based Linux.

## Installation
There is no install script of any sort at this time. Instead clone this repository
to the folder of your choice:
```
git clone https://github.com/mtijas/tomato-timer.git
```

## Dependencies
Tomato-timer uses python to run so it should obviously be installed.

Tomato-timer uses PyYAML package to read settings files. Install the package with pip:
```
pip install pyyaml
```

## Starting the program
Since there is no compiled binaries available the program should be started with python:
```
python src/TomatoTimer.py
```

## Configuration
Timers can be configured using YAML. The configuration file is searched from the current
folder of the timer. The default config file is named config.yml. User may also provide 
their own configuration file with the command line option `--config 'path/to/config.yml'`.

### Alarm type
Alarm type can be either 'beep' or 'flash'. 

- `beep` rings the terminal bell
- `flash` flashes the terminal window.

If terminal does not support selected type, then the other one is selected automatically
as a fallback.

### Use of colors
When `use_colors` is se to `True` the program will be beautifully decorated with 
meaningful colors for different types of timers:

- `work` is red
- `short break` is green
- `long break` is blue
- Any other type of timer will be yellow. 

Yes, you may call your alarms whatever you like (albeit they all will be yellow).
Set this `False` and the program will be plain black and white.

### Timers
Timers are configured as a dictionary with the key denoting the type of a timer and 
the number after that denoting the duration of said timer in minutes. Decimals are
also accepted (i.e. `work: 0.1` is a work timer lasting 6 seconds).

### Example

The example configuration file:
```yaml
alarm_type: "beep"
use_colors: True
timers:
  - work: 25
  - short break: 5
  - work: 25
  - short break: 5
  - work: 25
  - short break: 5
  - work: 25
  - long break: 35

```