#  Raspberry Pi Python Class for Chirp
Chirp is a capacitive soil moisture sensor with temperature and light sensor on board.

It is Open Hardware and is made by Albertas Mickėnas at Catnip Electronics.

For more information about Chirp:

https://github.com/Miceuz/i2c-moisture-sensor/

https://www.tindie.com/products/miceuz/i2c-soil-moisture-sensor/

## Features
>A trigger function to trigger all enabled sensors.
>
>Get soil moisture in percentage, requires calibration.
>
>Several temprature scales to choose from. Celcius, farenheit and kelvin.
>
>Temperature offset to calibrate temperature sensor.
>
>Change I2C address
>
>Deep sleep mode to save power.


Based on code by Jasper Wallace and Daniel Tamm

https://github.com/JasperWallace/chirp-graphite/blob/master/chirp.py

https://github.com/Miceuz/i2c-moisture-sensor/blob/master/README.md


# Documentation.

This is only a basic documentation, for more information please read the source code.

Python 2.6 or higher required due to @property and @function.setter

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
| temp_scale | str | 'celcius' | 'celcius', 'farenheit', 'kelvin' | Temperature scale to use. |
| temp_offset | float | 0 | | Offset for calibrating temperature.
| read_temp | bool | True | True or False | Enable or disable temp measurements.|
| read_moist | bool | True | True or False | Enable or disable moisture measurements. |
| read_light | bool | True |True or False | Enable or disable light measurements.


## Attributes


| attribute    | type | description             |
|:-------------|:-----|:------------------------|
| address | (int) | I2C address |
| busy_sleep | (float) | Sleep time in seconds while waiting for a new measurement. Default: 0.01 second |
| light | (int) | Light measurement. False if no measurement taken. |
| light_timestamp | (datetime) |Timestamp for light measurement. |
| max_moist | (int) | Calibrated maximum value for moisture, required for moist_percent |
| min_moist | (int) | Calibrated Minimum value for moisture, required for moist_percent |
| moist | (int) | Moisture measurement. False if no measurement taken. |
| moist_timestamp | (datetime) | Timestamp for moist measurement |
| read_light | (bool) | Set to True to enable light measurement, else False. |
| read_moist | (bool) | Set to True to enable moisture measurement, else False. |
| read_temp | (bool) | Set to True to enable temp measurement, else False. |
| temp | (float) | Temperature measurement. False if no measurement taken. |
| temp_offset | (float) | Offset for calibrating temperature. |
| temp_scale | (str) | Temperature scale to return. Valid: 'celsius', 'farenheit' or 'kelvin' |
| temp_timestamp | (datetime) | Timestamp for temp measurement. |


## Methods 

 
| method    | type | description   |
|:----------|:-----|:--------------|
| trigger() | | Triggers measurements on the activated sensor. | 
| reset() | | Reset sensor. | 
| sleep() | | Enter deep sleep mode. | 
| wake_up() | | Wakes up the sensor from deep sleep mode. | 
| moist_to_percent(int) | |  Convert a moisture capacitance value to percent. | 


### trigger()

``` python 
# Example
chirp.trigger()
```

Triggers measurements on the activated sensors.

### reset()

``` python 
# Example
chirp.reset() 
```

Reset sensor.

### sleep()

``` python 
# Example 
chirp.sleep() 
```

Enter deep sleep mode.

### wake_up(wake_time=1)

``` python 
# Example
chirp.wake_up() 
```

Wakes up the sensor from deep sleep mod.

Sending a reset to the sensor while in deep sleep mode usually fails.
But it triggers the sensor to wake up. We then wait for one second
for the sensor to wake up. Wake up time can be adjusted. Below one
second is not recommended, since it usually fails to retrieve the
first measurement(s) if it's lower than that.
Args:
wake_time (int, float, optional): Time in seconds for sensor to wake up.

### moist_to_percent(moisture)

``` python 
# Example 
percent = moist_to_percent(moisture) 
```

Convert a moisture capacitance value to percent using a calibrated
range for the sensor. Requires calibrated min_moist and max_moist
values. Useful when converting values not directly from the sensor,
ie from a database.
Args:
moisture (int): The capitance/moisture value recieved from the sensor.
Returns:
int: Moisture in percent
Raises:
ValueError: If min_moist and max_moist are not defined.

 ## Properties and setters 

Avaliable @property and @function.setter

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

Returns:
int: sensor firmware version

### @property busy

``` python 
# Example
if not chirp.busy
    do something...
```

Check if sensor is busy, returns True if busy, else Fals.

Returns:
bool: true if busy taking measurements, else False


### @property sensor_address

``` python
# Example
address = chirp.sensor_address 
```

Read I2C address from the sensor.

Returns:
int: I2C address

### @setter sensor_address

``` python 
# Example
chirp.sensor_address = new_address 
```


Set a new I2C address for the sensor.

Args:
new_addr (int): New I2C address. 3-119 or 0x03-0x77
Raises:
ValueError: If new_addr is not within required range.

### @property moist_percent

``` python 
# Example
    moisture = chirp.moist_percent 
```


Get moisture in percent.

Requires calibrated min_moist and max_moist values.
Returns:
int: Moisture in percent
Raises:
ValueError: If min_moist and max_moist are not defined.

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
## Advanced example with address change ability

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
