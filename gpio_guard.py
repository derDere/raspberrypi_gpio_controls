import RPi.GPIO as GPIO


class GPIO_G:
  def __enter__(self):
    GPIO.setmode(GPIO.BCM)

  def __exit__(self, type, value, traceback):
    GPIO.cleanup()
