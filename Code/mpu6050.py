"""
mpu6050.py - Minimal MicroPython driver for the MPU6050 6-axis IMU.

Purpose:
    Provides accelerometer and gyroscope measurements from the
    MPU6050 over the I2C bus.

Outputs:
    Accelerometer:
        ax, ay, az  -> acceleration in g

    Gyroscope:
        gx, gy, gz  -> angular velocity in degrees/second

Default MPU6050 ranges:
    Accelerometer: ±2g
    Gyroscope:     ±250 deg/s
"""

from machine import I2C

# ============================================================
# MPU6050 Register Addresses
# ============================================================

# Power management register
_PWR_MGMT_1 = const(0x6B)

# Device identification register
_WHO_AM_I = const(0x75)

# First accelerometer output register
_ACCEL_XOUT_H = const(0x3B)

# ============================================================
# Sensor Conversion Factors
# ============================================================

# Accelerometer sensitivity for ±2g range
# 16384 LSB = 1g
_ACCEL_SCALE = 16384.0

# Gyroscope sensitivity for ±250 deg/s range
# 131 LSB = 1 deg/s
_GYRO_SCALE = 131.0


class MPU6050:
    """
    MPU6050 sensor class.

    Handles:
        - Device initialization
        - Connection checking
        - Reading accelerometer values
        - Reading gyroscope values
    """

    def __init__(self, i2c: I2C, addr: int = 0x68):
        """
        Create MPU6050 object.

        Parameters:
            i2c  : initialized I2C bus
            addr : device I2C address (default 0x68)
        """

        self.i2c = i2c
        self.addr = addr

        # Wake up the MPU6050.
        # The device starts in sleep mode after power-up.
        self.i2c.writeto_mem(self.addr, _PWR_MGMT_1, b"\x00")

    def is_connected(self) -> bool:
        """
        Check whether the MPU6050 is responding on the I2C bus.

        Returns:
            True  -> valid device detected
            False -> device not detected
        """
        try:
            # Read WHO_AM_I register
            who = self.i2c.readfrom_mem(
                self.addr,
                _WHO_AM_I,
                1
            )[0]

            # Common MPU6050-compatible responses
            return who in (0x68, 0x70, 0x72, 0x73)

        except OSError:
            # I2C communication failed
            return False

    @staticmethod
    def _to_signed(hi, lo):
        """
        Convert two bytes into a signed 16-bit integer.

        Parameters:
            hi : high byte
            lo : low byte

        Returns:
            Signed integer value
        """

        # Combine bytes
        val = (hi << 8) | lo

        # Convert from unsigned to signed
        if val >= 0x8000:
            val -= 0x10000

        return val

    def read(self):
        """
        Read all accelerometer and gyroscope measurements.

        Returns:
            Dictionary containing:

            ax, ay, az -> acceleration in g
            gx, gy, gz -> angular velocity in deg/s
        """

        # Read 14 consecutive bytes starting at ACCEL_XOUT_H
        #
        # Memory layout:
        #   0,1   AX
        #   2,3   AY
        #   4,5   AZ
        #   6,7   TEMP
        #   8,9   GX
        #   10,11 GY
        #   12,13 GZ
        data = self.i2c.readfrom_mem(
            self.addr,
            _ACCEL_XOUT_H,
            14
        )

        # ----------------------------------------------------
        # Accelerometer data
        # Convert raw values to units of g
        # ----------------------------------------------------
        ax = self._to_signed(data[0], data[1]) / _ACCEL_SCALE
        ay = self._to_signed(data[2], data[3]) / _ACCEL_SCALE
        az = self._to_signed(data[4], data[5]) / _ACCEL_SCALE

        # Temperature bytes (6,7) are ignored

        # ----------------------------------------------------
        # Gyroscope data
        # Convert raw values to deg/s
        # ----------------------------------------------------
        gx = self._to_signed(data[8], data[9]) / _GYRO_SCALE
        gy = self._to_signed(data[10], data[11]) / _GYRO_SCALE
        gz = self._to_signed(data[12], data[13]) / _GYRO_SCALE

        # Return all sensor measurements in a dictionary
        return {
            "ax": ax,
            "ay": ay,
            "az": az,
            "gx": gx,
            "gy": gy,
            "gz": gz
        }
