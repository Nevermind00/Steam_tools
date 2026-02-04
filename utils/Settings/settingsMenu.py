import curses
import curses.panel
import json 
from loguru import logger

class SettingsMenu:
    def __init__(self):
        logger.remove()
        logger.add("logs/settingsMenu.log", rotation="500 MB")
        logger.info("Settings menu running")
        curses.wrapper(self.settings)

    def menu(self, stdscr):
        curses.curs_set(0)
        stdscr.keypad(True)

        self.menu_items = [
            "SPC",
            "View",
            "Keyboard",
            "Account",
            "Config",
            "About",
            "Exit"
        ]
        
        current_item = 0

        self.height, self.width = stdscr.getmaxyx()
        self.start_x = 0
        self.start_y = 0

        self.settings_menu = curses.newwin(self.width-90, self.height*3+1, self.start_y, self.start_x)

        self.settings_menu_panel = curses.panel.new_panel(self.settings_menu)

        while True:
            self.settings_menu.clear()
            self.settings_menu.border()

            self.title = "SPC"
            self.menu_title = "Settings"
            self.settings_menu.addstr(2, self.width//2 - len(self.title)//2, self.title, curses.A_BOLD)
            self.settings_menu.addstr(3, self.width//2 - len(self.menu_title)//2, self.menu_title, curses.A_BOLD)
            # Инструкция
            self.settings_menu.addstr(self.height-2, 2, "↑↓: Choice | Enter: Select | F8: Main Menu | F10: Exit")

            for idx, item in enumerate(self.menu_items):
                x = self.width//2 - len(item)//2 # Выравнивание x по центру
                y = self.height//2 - len(self.menu_items)//2 + idx # Выравнивание y по центру
                
                if idx == current_item:
                    # Выделенный пункт
                    self.settings_menu.addstr(y, x, f"> {item} <", curses.A_REVERSE)
                else:
                    # Невыделенный пункт 
                    self.settings_menu.addstr(y, x, f"  {item}  ")

            curses.panel.update_panels()
            stdscr.refresh()

            key = stdscr.getch()
            if key == curses.KEY_UP:
                current_item = (current_item - 1) % len(self.menu_items)
            elif key == curses.KEY_DOWN:
                current_item = (current_item + 1) % len(self.menu_items)
            elif key == ord('\n') or key == ord('\r'):  
                return current_item
            if key == curses.KEY_F10: 
                exit()
    
    def settings(self, stdscr):
        logger.remove()
        logger.add("/logs/settingsMenu.log", rotation="500 MB")

        curses.curs_set(0)
        self.select = self.menu(stdscr)

        if self.select == 0:
            stdscr.clear()
            stdscr.addstr(10, 10, "SPC")

        stdscr.refresh()
        stdscr.getch()

if __name__ == "__main__":
    ...
            