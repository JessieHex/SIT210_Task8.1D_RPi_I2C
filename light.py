from smbus import SMBus
import time
import sys

ADDR = 0x23 # Address of BH1750 at pin low,
            # can be viewed by "sudo i2cdetect -y 1"
MODE = 0x20 # One time high res mode, start measurement at 1lx resolution.
            # Measurement Time is typically 120ms.
            # It is automatically set to Power Down mode after measurement.
bus = SMBus(1) # System Management Bus is a interface. RPi and BH1750 communicate through it.


def main():
    while True:
        # read 2 bytes
        data = bus.read_word_data(ADDR, MODE)
        # RPi is little endian, while BH1750 is big endian
        # so we need to flip the bytes
        data = ((data & 0xff) << 8) | (data >> 8)
        brightness = data / 1.2 # from BH1750 datasheet
        if brightness < 20:
            print("Too dark")
        elif brightness >= 20 and brightness < 50:
            print("Dark")
        elif brightness >= 50 and brightness < 250:
            print("Medium")
        elif brightness >= 250 and brightness <500:
            print("Bright")
        else:
            print("Too bright")
        time.sleep(1) # sleep 1 sec

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
