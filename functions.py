from unicurses import *

KEY_ESC = 27
KEY_ESCAPE = KEY_ESC

global_color_number = 1;
global_styles = {}

def new_style( font_color, back_color ):
  global global_color_number, global_styles
  
  if (font_color, back_color) in global_styles:
    return global_styles[(font_color, back_color)]

  style = global_color_number
  init_pair(style, font_color, back_color)
  global_styles[(font_color, back_color)] = style
  
  global_color_number += 1
  return style

class unicurses_guard:
  def __enter__(self):
    stdscr = initscr()
    start_color()
    noecho()
    curs_set(False)
    keypad(stdscr, True)
    return stdscr
    
  def __exit__(self, type, value, traceback):
    endwin()
