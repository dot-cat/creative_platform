import RPi.GPIO as GPIO


class Motor(object):
    def __init__(self, pin_positive, pin_negative):
        if type(pin_negative) != int or type(pin_positive) != int:
            raise ValueError('Both arguments must be integers')

        self.pin_positive = pin_positive
        self.pin_negative = pin_negative

        GPIO.setup(self.pin_positive, GPIO.OUT)
        GPIO.setup(self.pin_negative, GPIO.OUT)

    def __del__(self):
        self.stop()
        GPIO.cleanup()

    def stop(self):
        GPIO.output(self.pin_negative, GPIO.LOW)
        GPIO.output(self.pin_positive, GPIO.LOW)

    def start_reverse(self):
        GPIO.output(self.pin_negative, GPIO.HIGH)
        GPIO.output(self.pin_positive, GPIO.LOW)

    def start_forward(self):
        GPIO.output(self.pin_negative, GPIO.LOW)
        GPIO.output(self.pin_positive, GPIO.HIGH)