# Raspberry Pi Python Class for Chirp
Chirp is a capacitive soil moisture sensor with temperature and light sensor on board.

It is Open Hardware and is made by Albertas Mickėnas at Catnip Electronics.

#### More information about Chirp:

https://github.com/Miceuz/i2c-moisture-sensor/

https://www.tindie.com/products/miceuz/i2c-soil-moisture-sensor/


## Features
* Uses a trigger function to trigger all enabled sensors. User selectable.

* Get soil moisture in percent (requires calibration) or capacitance value.

* Several temperature scales to choose from. Celsius, Farenheit and Kelvin.

* Offset to calibrate the temperature sensor.

* Measurement timestamps for all on board sensors.

* Built in support for changing the I2C address of the sensor.

* Deep sleep mode to conserve power.

* Calibration tool for soil moisture.

#### Created by @ageir, Göran Lundberg
Github: https://github.com/ageir/chirp-rpi/
#### Based on code by Jasper Wallace and Daniel Tamm

https://github.com/JasperWallace/chirp-graphite/blob/master/chirp.py

https://github.com/Miceuz/i2c-moisture-sensor/blob/master/README.md


# Documentation.

For more information please read the source code.

Python 2.6 or higher required.

## Calibration

To be able to retrieve the moisture in percent you need to calibrate the sensor.
The min_moist and max_moist values need to be defined. If these values are not adjusted properly for every induvidual sensor, the value for moist_percent might go below 0% and above 100%

You can use chirp.py to help calibrating your sensors.

```sh
# python chirp.py
```

Leave the dry sensor in dry air for a while so that the lowest value is recorded.


Then put the sensor in water so that it records the highest value.


The chirp.py program will automatically print out the highest and lowest value recorded when Ctrl-C is pressed.


Use these values for max_moist and min_moist.


Please note that these values might drift a little with temperature changes.
Make the calibration in the environment that you intend to use the sensor.

## Class definition

``` python 
 class Chirp(bus=1, address=0x20, min_moist=False, max_moist=False, temp_scale='celsius', temp_offset=0, read_temp=True, read_moist=True, read_light=True) 
```
## Arguments
| argument    | type | default | options | description |
|:-------------|:-----|:-----|:-----------------------|:-----|
| bus | int | 1 | | I2C bus|
| address | int | 0x20 | 3-119 or 0x03-0x77 | I2C address
| min_moist | int| False | | Set to a calibrated value to enable moist_percent |
| max_moist | int | False | | Set to a calibrated value to enable moist_percent
| temp_scale | str | 'celsius' | 'celsius', 'farenheit', 'kelvin' | Temperature scale to use. |
| temp_offset | float | 0 | | Offset for calibrating temperature.
| read_temp | bool | True | True or False | Enable or disable temp measurements.|
| read_moist | bool | True | True or False | Enable or disable moisture measurements. |
| read_light | bool | True |True or False | Enable or disable light measurements.


## Attributes


| attribute    | type | description             |
|:-------------|:-----|:------------------------|
| address | int | I2C address |
| busy_sleep | float | Sleep time in seconds while waiting for a new measurement. Default: 0.01 second |
| light | int | Light measurement. False if no measurement taken. |
| light_timestamp | datetime |Timestamp for light measurement. |
| max_moist | int | Calibrated maximum value for moisture, required for moist_percent |
| min_moist | int | Calibrated Minimum value for moisture, required for moist_percent |
| moist | int | Moisture measurement. False if no measurement taken. |
| moist_timestamp | datetime | Timestamp for moist measurement |
| read_light | bool | Set to True to enable light measurement, else False. |
| read_moist | bool | Set to True to enable moisture measurement, else False. |
| read_temp | bool | Set to True to enable temp measurement, else False. |
| temp | float | Temperature measurement. False if no measurement taken. |
| temp_offset | float | Offset for calibrating temperature. |
| temp_scale | str | Temperature scale for the temp attribute. Valid: 'celsius', 'farenheit' or 'kelvin' |
| temp_timestamp | datetime | Timestamp for the temperature measurement. |


## Methods 

 
| method    | description   |
|:----------|:--------------|
| trigger() | Triggers measurements on the activated sensor. | 
| reset() | Resets sensor. | 
| sleep() | Sets the sensor in deep sleep mode, to conserve power. | 
| wake_up() | Wakes the sensor up from deep sleep mode. | 
| moist_to_percent(int) | Convert a moisture capacitance value to percent. | 


### trigger()

``` python 
# Example
chirp.trigger()
```

Triggers measurements on the activated sensors. To select which sensors to trigger use the attributes read_moist, read_light, read_temp. Set them to True for enabled, False to disabled.

### reset()

``` python 
# Example
chirp.reset() 
```

Resets the sensor.

### sleep()

``` python 
# Example 
chirp.sleep() 
```

Puts the sensor in deep sleep mode to save power.

### wake_up(wake_time=1)

``` python 
# Example
chirp.wake_up() 
```

Wakes the sensor up from deep sleep mode.

```
Args:
wake_time (float, optional): Time in seconds for sensor to wake up.
```

Internal function:

Sends a command (get firmware version) to the sensor in deep sleep mode to wake it up.
The command fails, but it triggers the sensor to wake up. We then wait for one second
for the sensor to wake up. Wake up time can be adjusted. Below one
second is not recommended, since it usually fails to retrieve the
first measurement(s) if it's lower than that.

### moist_to_percent(moisture)

``` python 
# Example 
percent = chirp.moist_to_percent(moisture) 
```

Convert a moisture capacitance value to percent using a calibrated
range for the sensor. Requires calibrated min_moist and max_moist
values. Useful when converting values not directly from the sensor,
ie from a database.

```
Args:
moisture (int): The capitance/moisture value recieved from the sensor.

Returns:
int: Moisture in percent

Raises:
ValueError: If min_moist and max_moist are not defined.
```
 ## Properties and setters 

Avaliable properties and setters.

| property    | type | description   |
|:----------|:-----|:--------------|
| version | @property | Get firmware version for the sensor. | 
| busy | @property | Check if sensor is busy, returns True if busy, else False. | 
| sensor_address | @property | Read I2C address from the sensor. | 
| sensor_address | @setter | Set a new I2C address for the sensor. | 
| moist_percent | @property | Get moisture in percent. | 


### @property version

``` python 
# Example
firmware_version = chirp.version
```

Get firmware version for the sensor.

```
Returns:
int: sensor firmware version
```

### @property busy

``` python 
# Example
if not chirp.busy
    do something...
```

Check if sensor is busy, returns True if busy, else False.

```
Returns:
bool: true if busy taking measurements, else False
```

### @property sensor_address

``` python
# Example
address = chirp.sensor_address 
```

Read I2C address from the sensor.


```
Returns:
int: I2C address

```

### @setter sensor_address

``` python 
# Example
chirp.sensor_address = new_address 
```


Set a new I2C address for the sensor.


```
Args:
new_addr (int): New I2C address. 3-119 or 0x03-0x77

Raises:
ValueError: If new_addr is not within required range.
```

### @property moist_percent

``` python 
# Example
    moisture = chirp.moist_percent 
```

Get moisture in percent.

Requires calibrated min_moist and max_moist values.

If these values are not adjusted for your sensor the value for
moist_percent might go below 0% and above 100%


```
Returns:
int: Moisture in percent

Raises:
ValueError: If min_moist and max_moist are not defined.
```

# Example code

## Simple example
``` python
import chirp
import time

# These values needs to be calibrated for the percentage to work!
# The highest and lowest value the individual sensor outputs.
min_moist = 240
max_moist = 790

# Initialize the sensor.
chirp = chirp.Chirp(address=0x20,
                    read_moist=True,
                    read_temp=True,
                    read_light=True,
                    min_moist=min_moist,
                    max_moist=max_moist,
                    temp_scale='celsius',
                    temp_offset=0)

try:
    print('Moisture  | Temp   | Brightness')
    print('-' * 31)
    while True:
        # Trigger the sensors and take measurements.
        chirp.trigger()
        output = '{:d} {:4.1f}% | {:3.1f}°C | {:d}'
        output = output.format(chirp.moist, chirp.moist_percent,
                               chirp.temp, chirp.light)
        print(output)
        time.sleep(1)
except KeyboardInterrupt:
    print('\nCtrl-C Pressed! Exiting.\n')
finally:
    print('Bye!')

```
Example output:
```
Moisture  | Temp   | Brightness
-------------------------------
254  2.5% | 25.8°C | 8603
256  2.9% | 25.8°C | 8779
256  2.9% | 25.8°C | 8540
256  2.9% | 25.8°C | 8800
255  2.7% | 25.8°C | 8590
```

## Advanced example with address change ability and calibration

This code is included in chirp.py

``` python 
# Python 2.6 required.
if (sys.version_info < (2, 6)):
    python_version = ".".join(map(str, sys.version_info[:3]))
    print('Python version 2.6 or higher required, you are using \
        {}'.format(python_version))
    sys.exit()

# Prints usage information.
def print_usage():
    print('Usage:\n')
    print('{} <address> [[set] [new address]]\n'.format(sys.argv[0]))
    print('Examples:\n')
    print('Run continous measurements.')
    print('{} 0x20\n'.format(sys.argv[0]))
    print('Change the I2C address of the sensor on address 0x20 to 0x21')
    print('{} 0x20 set 0x21'.format(sys.argv[0]))
    print(len(sys.argv))
    sys.exit()

# Check command line argument for I2C address. (In hex, ie 0x20)
if (len(sys.argv) == 1) or (len(sys.argv) >= 5):
    print_usage()
if len(sys.argv) >= 2:
    if sys.argv[1].startswith("0x"):
        addr = int(sys.argv[1], 16)
    else:
        print_usage()

# Variables for calibrated max and min values. These need to be adjusted!
# These are only needed if you plan to use moist_percent.
# If these values are not adjusted for your sensor the value for
# moist_percent might go below 0% and above 100%
min_moist = 240
max_moist = 750

highest_measurement = False
lowest_measurement = False

# Initialize the sensor.
chirp = Chirp(address=addr,
              read_moist=True,
              read_temp=True,
              read_light=True,
              min_moist=min_moist,
              max_moist=max_moist,
              temp_scale='celsius',
              temp_offset=0)

# Check command line arguments if user wants to change the I2C address.
if len(sys.argv) >= 3:
    if sys.argv[2] == 'set':

        if sys.argv[3].startswith("0x"):
            new_addr = int(sys.argv[3], 16)
        else:
            new_addr = int(sys.argv[3])
        # Set new address, also resets the sensor.
        chirp.sensor_address = new_addr
        print('Chirp I2C address changed to {}'.format(hex(new_addr)))
        sys.exit()
    else:
        print_usage()

# Check which temperature sign to use.
if chirp.temp_scale == 'celsius':
    scale_sign = '°C'
elif chirp.temp_scale == 'farenheit':
    scale_sign = '°F'
elif chirp.temp_scale == 'kelvin':
    scale_sign = 'K'

print('Chirp soil moisture sensor.\n')
print('Firmware version:   {}'.format(hex(chirp.version)))
print('I2C address:        {}\n'.format(chirp.sensor_address))
print('Press Ctrl-C to exit.\n')
print('Moisture  | Temp   | Brightness')
print('-' * 31)

try:
    # Endless loop, taking measurements.
    while True:
        # Trigger the sensors and take measurements.
        chirp.trigger()
        output = '{:d} {:4.1f}% | {:3.1f}{} | {:d}'
        output = output.format(chirp.moist, chirp.moist_percent,
                               chirp.temp, scale_sign, chirp.light)
        print(output)
        # Adjust max and min measurement variables, used for calibrating
        # the sensor and allow using moisture percentage.
        if highest_measurement is not False:
            if chirp.moist > highest_measurement:
                highest_measurement = chirp.moist
        else:
            highest_measurement = chirp.moist
        if lowest_measurement is not False:
            if chirp.moist < lowest_measurement:
                lowest_measurement = chirp.moist
        else:
            lowest_measurement = chirp.moist
        time.sleep(1)
except KeyboardInterrupt:
    print('\nCtrl-C Pressed! Exiting.\n')
finally:
    print('Lowest moisture measured:  {}'.format(lowest_measurement))
    print('Highest moisture measured: {}'.format(highest_measurement))
    print('Bye!')

```
Example output:
```
Chirp soil moisture sensor.

Sensor version:   0x23
I2C address:      0x20

Press Ctrl-C to exit.

Moisture  | Temp   | Brightness
-------------------------------
251  2.2% | 28.5°C | 314
255  2.9% | 28.5°C | 337
254  2.7% | 28.5°C | 361
255  2.9% | 28.5°C | 371
255  2.9% | 28.5°C | 381
253  2.5% | 28.5°C | 269
^C
Ctrl-C Pressed! Exiting.

Lowest moisture measured: 251
Highest moisture measured: 255
Bye!

```
