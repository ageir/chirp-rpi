#  Raspberry Pi Python Class for Chirp capacitive soil moisture sensor.
Chirp is made by Catnip Electronics, Albertas Mickėnas
It has soil moisture, temperature and light sensors.

For more information about Chirp:
https://github.com/Miceuz/i2c-moisture-sensor
https://www.tindie.com/products/miceuz/i2c-soil-moisture-sensor/

Python Class by Göran Lundberg. https://github.com/GoranLundberg/chirp

Based on code by Jasper Wallace and Daniel Tamm
https://github.com/JasperWallace/chirp-graphite/blob/master/chirp.py
https://github.com/Miceuz/i2c-moisture-sensor/blob/master/README.md


# Chirp 

``` python 
 class Chirp(bus=1, address=0x20, min_moist=False, max_moist=False, temp_scale='celsius', temp_offset=0, read_temp=True, read_moist=True, read_light=True) 
```

##Attributes
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

--------- 

## Methods 

 
| method    | type | description   |
|:----------|:-----|:--------------|
| trigger() | | Triggers measurements on the activated sensor. | 
| version | @property | Get firmware version for the sensor. | 
| busy | @property | Check if sensor is busy, returns True if busy, else False. | 
| reset() | | Reset sensor. | 
| sleep() | | Enter deep sleep mode. | 
| wake_up() | | Wakes up the sensor from deep sleep mode. | 
| sensor_address | @property | Read I2C address from the sensor. | 
| sensor_address | @setter | Set a new I2C address for the sensor. | 
| moist_percent | @property | Get moisture in percent. | 
| moist_to_percent(int) | |  Convert a moisture capacitance value to percent. | 

 

### trigger

``` python 
    trigger() 
```


Triggers measurements on the activated sensor.

### @property version

``` python 
    version() 
```


Get firmware version for the sensor.

Returns:
int: sensor firmware version

### @property busy

``` python 
    busy() 
```


Check if sensor is busy, returns True if busy, else Fals.

Returns:
bool: true if busy taking measurements, else False

### reset

``` python 
    reset() 
```


Reset sensor.

### sleep

``` python 
    sleep() 
```


Enter deep sleep mode.

### wake_up

``` python 
    wake_up(wake_time=1) 
```


Wakes up the sensor from deep sleep mod.

Sending a reset to the sensor while in deep sleep mode usually fails.
But it triggers the sensor to wake up. We then wait for one second
for the sensor to wake up. Wake up time can be adjusted. Below one
second is not recommended, since it usually fails to retrieve the
first measurement(s) if it's lower than that.
Args:
wake_time (int, float, optional): Time in seconds for sensor to wake up.

### @property sensor_address

``` python 
    sensor_address() 
```


Read I2C address from the sensor.

Returns:
int: I2C address

### @setter sensor_address

``` python 
    sensor_address(new_addr) 
```


Set a new I2C address for the sensor.

Args:
new_addr (int): New I2C address. 3-119 or 0x03-0x77
Raises:
ValueError: If new_addr is not within required range.

### moist_percent

``` python 
    moist_percent() 
```


Get moisture in percent.

Requires calibrated min_moist and max_moist values.
Returns:
int: Moisture in percent
Raises:
ValueError: If min_moist and max_moist are not defined.

### moist_to_percent

``` python 
    moist_to_percent(moisture) 
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

