#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Class for the Chirp capacitive soil moisture sensor
    made by Catnip Electronics, Albertas Mickėnas

Links to Chirp:
https://github.com/Miceuz/i2c-moisture-sensor
https://www.tindie.com/products/miceuz/i2c-soil-moisture-sensor/

Python Class by Göran Lundberg. https://github.com/ageir/chirp

Based on code by Jasper Wallace and Daniel Tamm
https://github.com/JasperWallace/chirp-graphite/blob/master/chirp.py
https://github.com/Miceuz/i2c-moisture-sensor/blob/master/README.md
"""

from __future__ import division
from datetime import datetime

import smbus
import sys
import time


class Chirp(object):
    """Chirp soil moisture sensor with temperature and light sensors.

    Attributes:
        address (int): I2C address
        busy_sleep (float): Sleep time in seconds while waiting for a new
                            measurement. Default: 0.01 second
        light (int): Light measurement. False if no measurement taken.
        light_timestamp (datetime): Timestamp for light measurement.
        max_moist (int): Calibrated maximum value for moisture, required for moist_percent
        min_moist (int): Calibrated Minimum value for moisture, required for moist_percent
        moist (int): Moisture measurement. False if no measurement taken.
        moist_timestamp (datetime): Timestamp for moist measurement
        read_light (bool): Set to True to enable light measurement, else False.
        read_moist (bool): Set to True to enable moisture measurement, else False.
        read_temp (bool): Set to True to enable temp measurement, else False.
        temp (float): Temperature measurement. False if no measurement taken.
        temp_offset (float): Offset for calibrating temperature.
        temp_scale (str): Temperature scale to return. Valid: 'celsius', 'farenheit' or 'kelvin'
        temp_timestamp (datetime): Timestamp for temp measurement.
    """
    def __init__(self, bus=1, address=0x20, min_moist=False, max_moist=False,
                 temp_scale='celsius', temp_offset=0, read_temp=True,
                 read_moist=True, read_light=True):
        """Chir soil moisture sensor.

        Args:
            bus (int, optional): I2C bus. Default: 1
            address (int, optional): I2C address. Default: 0x20
            min_moist (bool, optional): Set to calibrated value to enable moist_percent
            max_moist (bool, optional): Set to calibrated value to enable moist_percent
            temp_scale (str, optional): Temperature scale to use. Default: 'celsius'
                                        Options: 'celsius', 'farenheit', 'kelvin'

            temp_offset (int, optional): Offset for calibrating temperature.
            read_temp (bool, optional): Enable or disable temp measurements.
                                        Default: True
            read_moist (bool, optional): Enable or disable moisture measurements.
                                         Default: True
            read_light (bool, optional): Enable or disable light measurements.
                                         Default: True
        """
        self.bus_num = bus
        self.bus = smbus.SMBus(bus)
        self.busy_sleep = 0.01
        self.address = address
        self.min_moist = min_moist
        self.max_moist = max_moist
        self.temp_scale = temp_scale
        self.temp_offset = temp_offset
        self.read_temp = read_temp
        self.read_moist = read_moist
        self.read_light = read_light
        self.temp = False
        self.moist = False
        self.light = False
        self.temp_timestamp = datetime
        self.moist_timestamp = datetime
        self.light_timestamp = datetime

        # Register values
        self._GET_CAPACITANCE = 0x00  # (r) 2 bytes
        self._SET_ADDRESS = 0x01      # (w) 1
        self._GET_ADDRESS = 0x02      # (r) 1
        self._MEASURE_LIGHT = 0x03    # (w) 0
        self._GET_LIGHT = 0x04        # (r) 2
        self._GET_TEMPERATURE = 0x05  # (r) 2
        self._RESET = 0x06            # (w) 0
        self._GET_VERSION = 0x07      # (r) 1
        self._SLEEP = 0x08            # (w) 0
        self._GET_BUSY = 0x09         # (r) 1

    def trigger(self):
        """Triggers measurements on the activated sensors
        """
        if self.read_temp is True:
            self.temp = self._read_temp()
        if self.read_moist is True:
            self.moist = self._read_moist()
        if self.read_light is True:
            self.light = self._read_light()

    def get_reg(self, reg):
        """Read 2 bytes from register

        Args:
            reg (int): Register number

        Returns:
            TYPE: 2 bytes
        """
        val = self.bus.read_word_data(self.address, reg)
        # return swapped bytes (they come in wrong order)
        return (val >> 8) + ((val & 0xFF) << 8)

    @property
    def version(self):
        """Get firmware version for the sensor.

        Returns:
            int: sensor firmware version
        """
        return self.bus.read_byte_data(self.address, self._GET_VERSION)

    @property
    def busy(self):
        """Check if sensor is busy, returns True if busy, else False

        Returns:
            bool: true if busy taking measurements, else False
        """
        busy = self.bus.read_byte_data(self.address, self._GET_BUSY)

        if busy == 1:
            return True
        else:
            return False

    def reset(self):
        """Reset sensor
        """
        self.bus.write_byte(self.address, self._RESET)

    def sleep(self):
        """Enter deep sleep mode
        """
        self.bus.write_byte(self.address, self._SLEEP)

    def wake_up(self, wake_time=1):
        """Wakes up the sensor from deep sleep mode

        Sends a command (get firmware version) to the sensor in deep sleep mode
        to wake it up. The command fails, but it triggers the sensor to wake up
        We then wait for one second for the sensor to wake up. Wake up time can
        be adjusted. Below one second is not recommended, since it usually
        fails to retrieve the first measurement(s) if it's lower than that.
        Args:
            wake_time (int, float, optional): Time in seconds for sensor to wake up.
        """
        self.wake_time = wake_time

        try:
            self.bus.read_byte_data(self.address, self._GET_VERSION)
        except OSError:
            pass
        finally:
            time.sleep(self.wake_time)

    @property
    def sensor_address(self):
        """Read I2C address from the sensor

        Returns:
            int: I2C address
        """
        return self.bus.read_byte_data(self.address, self._GET_ADDRESS)

    @sensor_address.setter
    def sensor_address(self, new_addr):
        """Set a new I2C address for the sensor

        Args:
            new_addr (int): New I2C address. 3-119 or 0x03-0x77

        Raises:
            ValueError: If new_addr is not within required range.
        """
        if isinstance(new_addr, int) and (new_addr >= 3 and new_addr <= 119):
            self.bus.write_byte_data(self.address, 1, new_addr)
            self.reset()
            self.address = new_addr
        else:
            raise ValueError('I2C address must be between 3-119 or 0x03-0x77.')

    @property
    def moist_percent(self):
        """Get moisture in percent.
        Requires calibrated min_moist and max_moist values.

        Returns:
            int: Moisture in percent

        Raises:
            ValueError: If min_moist and max_moist are not defined.
        """
        moisture = self.moist
        return self.moist_to_percent(moisture)

    def moist_to_percent(self, moisture):
        """ Convert a moisture capacitance value to percent using a calibrated
        range for the sensor. Requires calibrated min_moist and max_moist
        values. Useful when converting values not directly from the sensor,
        ie from a database.

        Args:
            moisture (int): The capitance/moisture value recieved from the sensor.
        Returns:
            int: Moisture in percent

        Raises:
            ValueError: If min_moist and max_moist are not defined.
        """
        if (self.min_moist or self.max_moist) is False:
            raise ValueError('min_moist and max_moist must be defined.')
        else:
            return round((((moisture - self.min_moist) /
                           (self.max_moist - self.min_moist)) * 100), 1)

    def _read_moist(self):
        """Read soil moisture (capacitance) from the sensor

        Returns:
            int: Soil moisture
        """
        # This returns last reading, and triggers a new. Discard old value.
        measurement = self.get_reg(self._GET_CAPACITANCE)

        # Wait for sensor to finish measurement
        while self.busy:
            time.sleep(self.busy_sleep)
        self.moist_timestamp = datetime.now()

        # Retrieve the measurement just triggered.
        measurement = self.get_reg(self._GET_CAPACITANCE)
        return measurement

    def _read_temp(self):
        """To read temperature, read 2 bytes from register 5. Returns degrees
        in celsius with one decimal. Adjusted for temperature offset

        Returns:
            float: Temperature in selected scale (temp_scale)

        Raises:
            ValueError: If temp_scale is not properly defined.
        """
        # This returns last reading, and triggers a new. Discard old value.
        measurement = self.get_reg(self._GET_TEMPERATURE)

        # Wait for sensor to finish measurement
        while self.busy:
            time.sleep(self.busy_sleep)
        self.temp_timestamp = datetime.now()

        # Retrieve the measurement just triggered.
        measurement = self.get_reg(self._GET_TEMPERATURE)

        # The chirp sensor returns an integer. But the return measurement is
        # actually a float with one decimal. Needs to be converted to float by
        # dividing by ten. And adjusted for temperature offset (if used).
        celsius = round(((measurement / 10) + self.temp_offset), 1)

        # Check which temperature scale to return the measurement in.
        if self.temp_scale == 'celsius':
            return celsius
        elif self.temp_scale == 'farenheit':
            # °F = (°C × 9/5) + 32
            farenheit = (celsius * 9 / 5) + 32
            return farenheit
        elif self.temp_scale == 'kelvin':
            # K = °C + 273.15
            kelvin = celsius + 273.15
            return kelvin
        else:
            raise ValueError(
                '{} is not a valid temperature scale. Only celsius, farenheit \
                and kelvin are supported.'.format(self.temp_scale))

    def _read_light(self):
        """ Measure light

        Returns:
            int: Light measurement, 0 - 65535 (0 is bright, 65535 is dark)
        """
        # Trigger a measurement
        self.bus.write_byte(self.address, self._MEASURE_LIGHT)

        # Wait for sensor to finish measurement. Takes longer in low light.
        while self.busy:
            time.sleep(self.busy_sleep)
        self.light_timestamp = datetime.now()
        measurement = self.get_reg(self._GET_LIGHT)
        return measurement

    def __repr__(self):
        """Summary

        Returns:
            str: repr
        """
        return '<Chirp sensor on bus {:d}, i2c addres {:d}>'.format(
            self.bus_num, self.address)


if __name__ == "__main__":
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
