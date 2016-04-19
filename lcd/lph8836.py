import spidev
#import RPIO
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
CS_LCD = 37

GPIO.setup(CS_LCD, GPIO.OUT, initial=GPIO.HIGH)


class hitachi(object):
    fonts = [0x3E, 0x50, 0x0A, 0x50, 0x3E]
    lcdIinitArray = [0x00, 0x00, 0x01, 0x07, 0x00, 0x00, 0x02, 0x04, 0x00, 0x04, 0x00, 0x00,
                     0x0C, 0x00, 0x01, 0x0D, 0x06, 0x16, 0x1E, 0x10, 0x10, 0x03, 0x00, 0x0C,
                     0x0E, 0x2D, 0x1F, 0x0D, 0x06, 0x16, 0x01, 0x02, 0x15, 0x0F, 0x00, 0x00,
                     0x0B, 0x00, 0x00, 0x11, 0x00, 0x00, 0x06, 0x00, 0x00, 0x05, 0x00, 0x30,
                     0x14, 0xAF, 0x00, 0x15, 0x00, 0x00, 0x16, 0x83, 0x00, 0x17, 0xAF, 0x00,
                     0x20, 0x00, 0x00, 0x30, 0x00, 0x00, 0x31, 0x04, 0x00, 0x32, 0x02, 0x07,
                     0x33, 0x07, 0x00, 0x34, 0x00, 0x05, 0x35, 0x07, 0x03, 0x36, 0x07, 0x07,
                     0x37, 0x00, 0x07, 0x3A, 0x12, 0x00, 0x3B, 0x00, 0x09, 0x07, 0x00, 0x05,
                     0x07, 0x00, 0x25, 0x07, 0x00, 0x27, 0x07, 0x00, 0x37]

    lph_rect_coord = [  [0x74, 0x00, 0x16],
                        [0x76, 131, 0],
                        [0x74, 0x00, 0x17],
                        [0x76, 18, 10],
                        [0x74, 0x00, 0x21],
                        [0x76, 10, 0]]

    def __cs_hi(self):
        GPIO.output(CS_LCD, GPIO.HIGH)
        time.sleep(0.01)

    def __cs_lo(self):
        GPIO.output(CS_LCD, GPIO.LOW)
        time.sleep(0.01)

    def __init__(self):
        self.h_fontbg = 0x00
        self.l_fontbg = 0x00
        self.h_fontcl = 0xFF
        self.l_fontcl = 0xFF
        self.spi = spidev.SpiDev()
        self.speed = 10000

        self.spi.open(0, 0)
        self.spi.max_speed_hz = self.speed
        self.__cs_hi()

    def __del__(self):
        GPIO.cleanup()

    def spi_send(self, data):
        self.spi.xfer([data])

    def lph_spi_com(self, lph_com):
        self.__cs_lo()
        self.spi_send(0x74)
        self.spi_send(0x00)
        self.spi_send(lph_com)
        self.__cs_hi()

    def lph_spi_dat(self, lph_dat_h, lph_dat_l):
        self.__cs_lo()
        self.spi_send(0x76)
        self.spi_send(lph_dat_h)
        self.spi_send(lph_dat_l)
        self.__cs_hi()

    def lcd_init(self):
        for i in range(0, 105, 3):
            self.lph_spi_com(self.lcdIinitArray[i])
            self.lph_spi_dat(self.lcdIinitArray[i + 1], self.lcdIinitArray[i + 2])
            time.sleep(0.1)

    def get_rect(self, x1, y1, x2, y2, lph_or):
        self.lph_spi_com(0x05)
        self.lph_spi_dat(0x00, lph_or)
        if lph_or == 0x28:
            self.lph_rect_coord[1][1] = 131 - y1
            self.lph_rect_coord[1][2] = 131 - y2
            self.lph_rect_coord[3][1] = x2
            self.lph_rect_coord[3][2] = x1
            self.lph_rect_coord[5][1] = x2
            self.lph_rect_coord[5][2] = 131 - y2
        else:
            self.lph_rect_coord[1][1] = x2
            self.lph_rect_coord[1][2] = x1
            self.lph_rect_coord[3][1] = y2
            self.lph_rect_coord[3][2] = y1
            self.lph_rect_coord[5][1] = x1
            self.lph_rect_coord[5][2] = y1
        for i in range(0, 6):
            self.__cs_lo()
            self.spi_send(self.lph_rect_coord[i][0])
            self.spi_send(self.lph_rect_coord[i][1])
            self.spi_send(self.lph_rect_coord[i][2])
            self.__cs_hi()
        self.lph_spi_com(0x22)

    def fill_rect(self, hRGB, lRGB):
        self.__cs_lo()
        self.spi_send(0x76)
        for i in range(0, 23232):
            self.spi_send(hRGB)
            self.spi_send(lRGB)
        self.__cs_hi()

    def fill_rect_size(self, hRGB, lRGB, size):
        self.self.__cs_lo()
        self.spi_send(0x76)
        for i in range(0, size):
            self.spi_send(hRGB)
            self.spi_send(lRGB)
            self.__cs_hi()

    def fill_bitmap(self, lph_bmp_pic, w):
        if w > 0 and lph_bmp_pic != 0:
            self.__cs_lo()
            self.spi_send(0x76)
            for lph_bmp_j in range(0, w):
                self.spi_send(lph_bmp_pic[lph_bmp_j])
            self.__cs_hi()
            return 0
        else:
            return 1

    def set_point(self, x1, y1, hRGB, lRGB):
        self.get_rect(x1, y1, x1 + 1, y1 + 1, 0x30)
        self.lph_spi_dat(hRGB, lRGB)


if __name__ == '__main__':
    lcd = hitachi()
    lcd.lcd_init()
    while True:
        lcd.lcd_init()
#VDD+ = 17
#SCLK = 23
#SDIN = 19
#D/C = 15
#SCE = 13
#GND - =9