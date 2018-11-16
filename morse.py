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
  result = ""
  for b in morse:
    if b:
      result += "="
    else:
      result += "_"
  return result

def outMorse(morse, IO, doPrint = False, speed = 0.125):
  with GPIO_G():
    gpio.setmode(gpio.BCM)
    gpio.setup(IO, gpio.OUT)
    gpio.output(IO, False)
    for b in morse:
      gpio.output(IO, b)
      if doPrint:
        if b:
          sys.stdout.write("=")
        else:
          sys.stdout.write("_")
        sys.stdout.flush()
      T.sleep(speed)
    print("")

def main(argv):
  for arg in argv:
    m = str2morse(arg)
    #print(displayMorse(m))
    outMorse(m, 3, True)

if __name__=="__main__":
  if len(sys.argv) > 1:
    main(sys.argv[1:])
  else:
    main([])
