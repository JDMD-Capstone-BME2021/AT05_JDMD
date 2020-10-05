# Technical Requirements

*Daniil Shuraev – October 4, 2020*

*version 0.1*

## Architecture Overview

The program is to consist of 6 core modules

1. Image acquisition module
2. Light control module
3. Motor control module
4. Reconstruction module
5. Core
6. GUI

## Image Acquisition Module

IAM must functionality to capture real time video feed from the camera as well as take photos on call.

### Interface

```python
def get_frame():
    pass
```

## Light Control Module

LCM must provide functionality to set light intensity independently for each of the three light channels.

### Interface

```python
def set_intensity(channel: int, intensity: int):
    pass

def switch_off(channel: int):
    pass

def switch_off():
    pass

def switch_on(channel: int):
    pass

def switch_on():
    pass

CHANNEL1 = 1 #  001
CHANNEL2 = 2 #	010
CHANNEL3 = 4 #	100

MIN_INTENSITY = 0
MAX_INTENSITY = 255
```

`channel` is a bit field which selects the channel to set the light intensity to, for example

```python
set_intensity(CHANNEL1|CHANNEL2, 100)
```

`intensity` should be controlled in 1/256 increments from 0 to 255.

`switch_off(channel)` should set intensity on selected channel(s) to `MIN_INTENSITY`

`switch_off()` should set intensity on all channels to `MIN_INTENSITY`

`switch_on(channel)` should set intensity on selected channel(s) to `MAX_INTENSITY`

## Motor Control Unit

MCU must provide functionality to set platform rotation to a specified angle between $0^\circ$ and $360^\circ$ with $.5^\circ$ precision.

### Interface

```python
def set_position(angle: float):
    pass

def reset():
    pass
```

## Reconstruction Module

RM should provide functionality to reconstruct a tomographic image from the supplied set of images.

```python
def reconstruct(imgs) -> numpy.array:
    pass
```

## Core

Core must performs synchronization between control units.

Core must provide functionality to 

- take a specified number of pictures evenly spaced between two specified angles
- receive video feed
- call reconstruction routine
- save input, output or sinogram
- save system parameters
- load input
- load system parameters
- load from command line arguments (?)
- reset system

```python
def get_images(nimg: int, start=0: float, end=180: float):
    pass

def get_image():
    pass

def reset():
    pass
```

## GUI

GUI should provide a wrapper for Control Unit