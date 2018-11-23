import argparse
from gpio_guard import *
import RPi.GPIO as gpio
import time as T
import sys

ALPHABET = {
  "A": [1, 3],
  "B": [3, 1, 1, 1],
  "C": [3, 1, 3, 1],
  "D": [3, 1, 1],
  "E": [1],
  "F": [1, 1, 3, 1],
  "G": [3, 3, 1],
  "H": [1, 1, 1, 1],
  "I": [1, 1],
  "J": [1, 3, 3, 3],
  "K": [3, 1, 3],
  "L": [1, 3, 1, 1],
  "M": [3, 3],
  "N": [3, 1],
  "O": [3, 3, 3],
  "P": [1, 3, 3, 1],
  "Q": [3, 3, 1, 3],
  "R": [1, 3, 1],
  "S": [1, 1, 1],
  "T": [3],
  "U": [1, 1, 3],
  "V": [1, 1, 1, 3],
  "W": [1, 3, 3],
  "X": [3, 1, 1, 3],
  "Y": [3, 1, 3, 3],
  "Z": [3, 3, 1, 1],
  "1": [1, 3, 3, 3, 3],
  "2": [1, 1, 3, 3, 3],
  "3": [1, 1, 1, 3, 3],
  "4": [1, 1, 1, 1, 3],
  "5": [1, 1, 1, 1, 1],
  "6": [3, 1, 1, 1, 1],
  "7": [3, 3, 1, 1, 1],
  "8": [3, 3, 3, 1, 1],
  "9": [3, 3, 3, 3, 1],
  "0": [3, 3, 3, 3, 3],
  "Å": [1, 3, 3, 1, 3],
  "Å": [1, 3, 3, 1, 3],
  "Ä": [1, 3, 1, 3],
  "È": [1, 3, 1, 1, 3],
  "É": [1, 1, 3, 1, 1],
  "Ö": [3, 3, 3, 1],
  "Ü": [1, 1, 3, 3],
  "ß": [1, 1, 1, 3, 3, 1, 1],
  "Ñ": [3, 3, 1, 3, 3],
  ".": [1, 3, 1, 3, 1, 3],
  ",": [3, 3, 1, 1, 3, 3],
  ":": [3, 3, 3, 1, 1, 1],
  ";": [3, 1, 3, 1, 3, 1],
  "?": [1, 1, 3, 3, 1, 1],
  "-": [3, 1, 1, 1, 1, 3],
  "_": [1, 1, 3, 3, 1, 3],
  "(": [3, 1, 3, 3, 1],
  ")": [3, 1, 3, 3, 1, 3],
  "'": [1, 3, 3, 3, 3, 1],
  "=": [3, 1, 1, 1, 3],
  "+": [1, 3, 1, 3, 1],
  "/": [3, 1, 1, 3, 1],
  "@": [1, 3, 3, 1, 3, 1]
}

ON = "■"
OFF = "·"

DEF_SPEED = 0.15
DEF_GPIO = 3

def str2morse(str):
  str = str.upper()
  result = []
  for c in str:
    if c == " ":
      result += [False,False,False,False]
    elif c in ALPHABET:
      for l in ALPHABET[c]:
        for i in range(l):
          result += [True]
        result += [False]
      result += [False,False]
  result += [False,False,False,False]
  return result

def displayMorse(morse):
  global ON, OFF
  result = ""
  for b in morse:
    if b:
      result += ON
    else:
      result += OFF
  return result

def outMorse(morse, IO = DEF_GPIO, doPrint = True, speed = DEF_SPEED):
  #global ON, OFF
  with GPIO_G():
    gpio.setmode(gpio.BCM)
    gpio.setup(IO, gpio.OUT)
    gpio.output(IO, False)
    for b in morse:
      gpio.output(IO, b)
      if doPrint:
        if b:
          sys.stdout.write(ON)
        else:
          sys.stdout.write(OFF)
        sys.stdout.flush()
      T.sleep(speed)
    print("")

def main(argv):
  print(str(argv)[10:-1])
  run = True
  while run:
    for arg in argv.morse:
      m = str2morse(arg)
      #print(displayMorse(m))
      outMorse(m, int(argv.gpio), True, float(argv.speed))
    run = argv.repeat

if __name__=="__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('morse', nargs='+', help="Here goes the data that shall be displayed as morse code.")
  parser.add_argument('-s','--speed', default=DEF_SPEED, required=False, help="Sets the speed which is used to display the morse code. Default: " + str(DEF_SPEED) + " sec")
  parser.add_argument('-io','--gpio', default=DEF_GPIO, required=False, help="Sets the GPIO which is used to output the morse code. Default: "+ str(DEF_GPIO))
  parser.add_argument('-r','--repeat', required=False, action='store_true', help="...")

  args = parser.parse_args()
  
  try:  
    main(args)
  except KeyboardInterrupt:
    print("\nTransmission canceled!")

