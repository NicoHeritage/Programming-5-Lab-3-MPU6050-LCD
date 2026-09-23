"""
i2c_lcd.py - Minimal MicroPython driver for a 16x2 HD44780 LCD
using a PCF8574 I2C backpack.

Purpose:
    Allows an ESP32 to control an LCD display over I2C instead
    of using many parallel GPIO pins.

PCF8574 Backpack Pin Mapping:
    P0 -> RS (Register Select)
    P1 -> RW (Read/Write)
    P2 -> EN (Enable)
    P3 -> Backlight Control
    P4 -> D4
    P5 -> D5
    P6 -> D6
    P7 -> D7

The LCD operates in 4-bit mode, meaning each byte is sent
as two 4-bit transfers (nibbles).
"""

from machine import I2C
import utime

# ============================================================
# PCF8574 Control Bit Definitions
# ============================================================

# Register Select:
# 0 = command
# 1 = character data
_RS = const(0x01)

# Enable line for LCD communication
_EN = const(0x04)

# LCD backlight control bit
_BL = const(0x08)


class I2cLcd:
    """
    LCD Driver Class

    Provides functions to:
        - Initialize LCD
        - Clear display
        - Move cursor
        - Display text
    """

    def __init__(self,
                 i2c: I2C,
                 addr: int = 0x27,
                 cols: int = 16,
                 rows: int = 2):
        """
        Create LCD object.

        Parameters:
            i2c  : initialized I2C bus
            addr : I2C address of PCF8574 backpack
            cols : number of LCD columns
            rows : number of LCD rows
        """

        self.i2c = i2c
        self.addr = addr
        self.cols = cols
        self.rows = rows

        # Backlight enabled by default
        self.backlight = _BL

        # Initialize LCD hardware
        self._init_display()

    # ========================================================
    # Low-Level PCF8574 Functions
    # ========================================================

    def _write_byte(self, data):
        """
        Send one byte to the PCF8574.

        The backlight bit is always preserved.
        """
        self.i2c.writeto(
            self.addr,
            bytes([data | self.backlight])
        )

    def _pulse_enable(self, data):
        """
        Generate an Enable pulse.

        The LCD reads incoming data on the EN transition.
        """

        self._write_byte(data | _EN)
        utime.sleep_us(1)

        self._write_byte(data & ~_EN)
        utime.sleep_us(50)

    def _write4(self, nibble, rs):
        """
        Send a 4-bit value to the LCD.

        Parameters:
            nibble : upper or lower 4 bits
            rs     : False = command
                     True  = character data
        """

        data = (nibble << 4) | (_RS if rs else 0)

        self._write_byte(data)
        self._pulse_enable(data)

    def _write_cmd(self, cmd):
        """
        Send an LCD command byte.

        Commands are sent as two 4-bit transfers.
        """

        # Upper nibble
        self._write4(cmd >> 4, rs=False)

        # Lower nibble
        self._write4(cmd & 0x0F, rs=False)

        utime.sleep_us(50)

    def _write_char(self, ch):
        """
        Send one ASCII character to the LCD.
        """

        # Upper nibble
        self._write4(ch >> 4, rs=True)

        # Lower nibble
        self._write4(ch & 0x0F, rs=True)

        utime.sleep_us(50)

    # ========================================================
    # LCD Initialization
    # ========================================================

    def _init_display(self):
        """
        Initialize the HD44780 LCD.

        This follows the standard 4-bit startup sequence
        specified in the HD44780 datasheet.
        """

        # Wait for LCD power-up
        utime.sleep_ms(50)

        # Reset sequence
        self._write4(0x03, rs=False)
        utime.sleep_ms(5)

        self._write4(0x03, rs=False)
        utime.sleep_us(150)

        self._write4(0x03, rs=False)

        # Switch to 4-bit mode
        self._write4(0x02, rs=False)

        # Function Set:
        # 4-bit mode, 2 display lines, 5x8 font
        self._write_cmd(0x28)

        # Display ON
        # Cursor OFF
        # Blink OFF
        self._write_cmd(0x0C)

        # Clear display contents
        self.clear()

        # Entry mode:
        # Cursor moves right after each character
        self._write_cmd(0x06)

    # ========================================================
    # Public Functions
    # ========================================================

    def clear(self):
        """
        Clear the LCD display and return cursor to home.
        """

        self._write_cmd(0x01)

        # Clear command takes longer to execute
        utime.sleep_ms(2)

    def set_cursor(self, col, row):
        """
        Move cursor to a specified column and row.

        Parameters:
            col : horizontal position
            row : vertical position
        """

        # DDRAM addresses for each row
        row_offsets = (
            0x00,
            0x40,
            0x14,
            0x54
        )

        self._write_cmd(
            0x80 | (col + row_offsets[row])
        )

    def putstr(self, text):
        """
        Display a string on the LCD.

        Parameters:
            text : text to display
        """

        for ch in text:
            self._write_char(ord(ch))
