import RPi.GPIO as G
from gpio_guard import *
#import json
from unicguard import *


class GPIO:
  def __init__(self, IO, Style, Text):
    self.IO = IO
    self.Style = Style
    self.Text = Text
    self.ON = False
    if self.IO != 0:
      G.setup(self.IO, G.OUT)
      G.output(self.IO, False)

  def toggle(self):
    if self.ON:
      self.turnOFF()
    else:
      self.turnON()

  def turnON(self):
    if self.IO != 0:
      self.ON = True
      G.output(self.IO, G.HIGH)

  def turnOFF(self):
    if self.IO != 0:
      self.ON = False
      G.output(self.IO, G.LOW)


IOW = 9  # GPIO Width
IOH = 1  # GPIO Height
IOM = 0  # GPIO Margin
WIX = 1  # Window X
WIY = 1  # Window Y
WIPT = 1 # Window Padding Top
WIPB = 1 # Window Padding Bottom
WIPL = 1 # Window Padding Left
WIPR = 1 # Window Padding Right
WICS = 6 # Window Center Space


class Board:
  def __init__(self):
    self.styles = {
      "pwr": COLOR_PAIR(new_style(COLOR_BLUE,    COLOR_WHITE)),
      "io":  COLOR_PAIR(new_style(COLOR_GREEN,   COLOR_WHITE)),
      "gnd": COLOR_PAIR(new_style(COLOR_BLACK,   COLOR_WHITE)),
      "id":  COLOR_PAIR(new_style(COLOR_MAGENTA, COLOR_WHITE)),
      "5v":  COLOR_PAIR(new_style(COLOR_RED,     COLOR_WHITE)),
      "box": COLOR_PAIR(new_style(COLOR_BLACK,   COLOR_WHITE))
    }
    self.IOs = [
      [ GPIO(0, "pwr","+3.3V PWR"), GPIO(0, "5v","+5V PWR")],
      [ GPIO(2, "io", "GPIO 2"),    GPIO(0, "5v","+5V PWR")],
      [ GPIO(3, "io", "GPIO 3"),    GPIO(0, "gnd","Ground") ],
      [ GPIO(4, "io", "GPIO 4"),    GPIO(14,"io", "GPIO 14")],
      [ GPIO(0, "gnd","Ground"),    GPIO(15,"io", "GPIO 15")],
      [ GPIO(17,"io", "GPIO 17"),   GPIO(18,"io", "GPIO 18")],
      [ GPIO(27,"io", "GPIO 27"),   GPIO(0, "gnd","Ground") ],
      [ GPIO(22,"io", "GPIO 22"),   GPIO(23,"io", "GPIO 23")],
      [ GPIO(0, "pwr","+3.3V PWR"), GPIO(24,"io", "GPIO 24")],
      [ GPIO(10,"io", "GPIO 10"),   GPIO(0, "gnd","Ground") ],
      [ GPIO(9, "io", "GPIO 9"),    GPIO(25,"io", "GPIO 25")],
      [ GPIO(11,"io", "GPIO 11"),   GPIO(8, "io", "GPIO 8") ],
      [ GPIO(0, "gnd","Ground"),    GPIO(7, "io", "GPIO 7") ],
      [ GPIO(0, "id", "ID_SD"),     GPIO(0, "id", "ID_SC")  ],
      [ GPIO(5, "io", "GPIO 5"),    GPIO(0, "gnd","Ground") ],
      [ GPIO(6, "io", "GPIO 6"),    GPIO(12,"io", "GPIO 12")],
      [ GPIO(13,"io", "GPIO 13"),   GPIO(0, "gnd","Ground") ],
      [ GPIO(19,"io", "GPIO 19"),   GPIO(16,"io", "GPIO 16")],
      [ GPIO(26,"io", "GPIO 26"),   GPIO(20,"io", "GPIO 20")],
      [ GPIO(0, "gnd","Ground"),    GPIO(21,"io", "GPIO 21")]
    ]
    self.wins = {}
    self.pans = {}
    self.selection = [0,1]

    self.BGwin = newwin((((IOH + IOM)*len(self.IOs))-IOM)+WIPB+WIPT, IOW*2+WIPL+WIPR+WICS, WIY, WIX)
    self.BGpan = new_panel(self.BGwin)
    wbkgd(self.BGwin,  ord(' '), self.styles["gnd"])

    self.SEwin = newwin(IOH, WIPL + IOW + WIPR, WIY + WIPT, WIX)
    self.SEpan = new_panel(self.SEwin)
    wbkgd(self.SEwin,  ord('='), self.styles["box"])
    top_panel(self.SEpan)

    self.IOwin = newwin((IOH + IOM)*len(self.IOs), 2, WIPT + WIY, WIPL + IOW + int((WICS/2)-1) + WIX)
    self.IOpan = new_panel(self.IOwin)

    for y in range(len(self.IOs)):
      for x in range(2):
        win = newwin(IOH, IOW, (IOH+IOM)*y+WIPT+WIY, IOW*x+WIPL+(WICS*x)+WIX)
        pan = new_panel(win)
        self.wins[(x,y)] = win
        self.pans[(x,y)] = pan
        gpio = self.IOs[y][x]
        wbkgd(win,  ord(' '), self.styles[gpio.Style])
        if x == 0:
          waddstr(win, ((' ' * IOW) + gpio.Text)[-IOW:])
        else:
          waddstr(win, gpio.Text)
    self.update()

  def update(self):
    move_panel(self.SEpan, (self.selection[1] * (IOH + IOM)) + WIY + WIPT, (self.selection[0] * (IOW + WICS)) + WIX)
    wmove(self.SEwin, 0, 0)
    wbkgd(self.IOwin,  ord(' '), self.styles["gnd"])
    wmove(self.IOwin, 0, 0)
    for y in range(len(self.IOs)):
      waddstr(self.IOwin, "  "*(IOH-1))
      for x in range(2):
        win = self.wins[(x,y)]
        gpio = self.IOs[y][x]
        if gpio.IO == 0:
          waddstr(self.IOwin, "O", self.styles[gpio.Style])
        else:
          if gpio.ON:
            waddstr(self.IOwin, "1", self.styles[gpio.Style] + A_STANDOUT)
          else:
            waddstr(self.IOwin, "0", self.styles[gpio.Style])
      waddstr(self.IOwin, "  "*IOM)
    update_panels()
    doupdate()


def main(args):
  with GPIO_G():
    with unicurses_guard() as stdscr:
      b = Board()
      input = None
      while input != ord('q'):
        input = getch()
        if input == KEY_UP:
          b.selection[1] -= 1
        elif input == KEY_DOWN:
          b.selection[1] += 1
        elif input == KEY_LEFT:
          b.selection[0] -= 1
        elif input == KEY_RIGHT:
          b.selection[0] += 1
        elif input == ord(' '):
          b.IOs[b.selection[1]][b.selection[0]].toggle()
        b.selection[1] %= len(b.IOs)
        b.selection[0] %= 2
        b.update()


if __name__ == "__main__":
  import sys
  if len(sys.argv) > 0:
    main(sys.argv[1:])
  else:
    main()
