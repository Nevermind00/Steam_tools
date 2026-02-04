import curses
import _curses_panel
from loguru import logger 

class SPCSETTINGS:
    def __init__(self):
        ...
    
    def Menu(self, stdscr, y, x, prompt, length):
        curses.curs_set(0)
        stdscr.keypad(True)

        self.height, self.width = stdscr.getmaxyx()

        menu = curses.newwin()
         