"""
main.py - IoT Stack Lab: 6-axis IMU -> I2C LCD (MicroPython / ESP32-S3)

Hardware:
    - ESP32-S3 DevKitC-1
    - LCD1602 with PCF8574 I2C backpack
    - MPU6050 IMU

I2C Connections:
    SDA -> GPIO8
    SCL -> GPIO9

Program Operation:
    1. Initialize I2C bus
    2. Initialize LCD display
    3. Initialize MPU6050 IMU
    4. Verify IMU is connected
    5. Continuously:
        - Read accelerometer and gyroscope data
        - Calculate pitch and roll angles
        - Estimate yaw angle using gyro integration
        - Alternate LCD screens every 1.5 seconds
        - Print measurements to the serial terminal
"""

# Mathematical functions for trigonometry calculations
import math

# Time-related functions for delays and timing
import utime

# Hardware interfaces
from machine import I2C, Pin

# Custom MPU6050 driver
from mpu6050 import MPU6050

# Custom I2C LCD driver
from i2c_lcd import I2cLcd


# ============================================================
# Configuration Settings
# ============================================================

# I2C bus number
I2C_ID = 0

# ESP32-S3 I2C pin assignments
I2C_SDA = 8
I2C_SCL = 9

# Standard I2C communication speed
I2C_FREQ = 100_000

# LCD I2C address (commonly 0x27)
LCD_ADDR = 0x27

# LCD dimensions
LCD_COLS = 16
LCD_ROWS = 2

# Sensor sample period (ms)
SAMPLE_MS = 200

# LCD page-switch interval (ms)
SCREEN_SWAP_MS = 1500


def main():
    """
    Main program entry point.
    Initializes hardware and continuously updates sensor data.
    """

    # --------------------------------------------------------
    # Create I2C interface
    # --------------------------------------------------------
    i2c = I2C(
        I2C_ID,
        sda=Pin(I2C_SDA),
        scl=Pin(I2C_SCL),
        freq=I2C_FREQ
    )

    # --------------------------------------------------------
    # Initialize LCD
    # --------------------------------------------------------
    lcd = I2cLcd(i2c, LCD_ADDR, LCD_COLS, LCD_ROWS)
    lcd.putstr("Init IMU...")

    # --------------------------------------------------------
    # Initialize IMU
    # --------------------------------------------------------
    imu = MPU6050(i2c)

    # --------------------------------------------------------
    # Verify IMU connection
    # --------------------------------------------------------
    if not imu.is_connected():

        # Error path if IMU is not detected
        lcd.clear()
        lcd.putstr("IMU NOT FOUND")

        lcd.set_cursor(0, 1)
        lcd.putstr("Check wiring")

        print("[ERROR] MPU6050 not detected on I2C bus.")

        # Halt indefinitely until fixed
        while True:
            utime.sleep(1)

    # --------------------------------------------------------
    # System startup successful
    # --------------------------------------------------------
    lcd.clear()
    print("System ready. Streaming 6-axis data...")

    # Estimated heading (degrees)
    yaw = 0.0

    # Track which LCD screen is displayed
    show_accel_screen = True

    # Timing variables
    last_sample = utime.ticks_ms()
    last_switch = utime.ticks_ms()

    # ========================================================
    # Main Loop
    # ========================================================
    while True:

        # Current time
        now = utime.ticks_ms()

        # Time since last sample
        elapsed = utime.ticks_diff(now, last_sample)

        # Maintain fixed sampling rate
        if elapsed < SAMPLE_MS:
            utime.sleep_ms(SAMPLE_MS - elapsed)
            now = utime.ticks_ms()

        # Calculate actual sample interval in seconds
        dt = utime.ticks_diff(now, last_sample) / 1000.0

        # Update sample timestamp
        last_sample = now

        # ----------------------------------------------------
        # Read IMU measurements
        # ----------------------------------------------------
        d = imu.read()

        # Convert acceleration from g to m/s²
        ax = d["ax"] * 9.80665
        ay = d["ay"] * 9.80665
        az = d["az"] * 9.80665

        # Gyroscope Z-axis angular velocity (deg/s)
        gz = d["gz"]

        # ----------------------------------------------------
        # Calculate Roll Angle
        # ----------------------------------------------------
        # Uses gravity vector measured by accelerometer
        roll = math.atan2(ay, az) * 180.0 / math.pi

        # ----------------------------------------------------
        # Calculate Pitch Angle
        # ----------------------------------------------------
        pitch = (
            math.atan2(
                -ax,
                math.sqrt(ay * ay + az * az)
            ) * 180.0 / math.pi
        )

        # ----------------------------------------------------
        # Estimate Yaw Angle
        # ----------------------------------------------------
        # No magnetometer available, therefore yaw is
        # estimated by integrating gyro Z measurements.
        # This method accumulates drift over time.
        yaw += gz * dt

        # Keep yaw between -180° and +180°
        if yaw > 180:
            yaw -= 360

        if yaw < -180:
            yaw += 360

        # ----------------------------------------------------
        # Alternate LCD display pages
        # ----------------------------------------------------
        if utime.ticks_diff(now, last_switch) > SCREEN_SWAP_MS:
            show_accel_screen = not show_accel_screen
            last_switch = now
            lcd.clear()

        # ----------------------------------------------------
        # Update LCD Display
        # ----------------------------------------------------
        lcd.set_cursor(0, 0)

        if show_accel_screen:

            # Screen 1: Acceleration values
            lcd.putstr("X:{:.1f} Y:{:.1f}".format(ax, ay))

            lcd.set_cursor(0, 1)
            lcd.putstr("Z:{:.1f} m/s2".format(az))

        else:

            # Screen 2: Orientation estimates
            lcd.putstr("P:{:.0f} R:{:.0f}".format(pitch, roll))

            lcd.set_cursor(0, 1)
            lcd.putstr("Yaw:{:.0f}".format(yaw))

        # ----------------------------------------------------
        # Serial Output (proof-of-test)
        # ----------------------------------------------------
        print(
            "AX:{:.2f} AY:{:.2f} AZ:{:.2f} "
            "Pitch:{:.1f} Roll:{:.1f} Yaw:{:.1f}"
            .format(
                ax,
                ay,
                az,
                pitch,
                roll,
                yaw
            )
        )


# ============================================================
# Program Start
# ============================================================
main()