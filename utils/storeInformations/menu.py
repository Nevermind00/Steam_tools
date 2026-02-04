import curses
import curses.panel
from loguru import logger

from .wishlistFindGame import GameInfo

class WishlistMenu:
    def __init__(self):
        curses.wrapper(self.Whishlist_menu)
    
    def menu(self, stdscr):
        #Отключение курсора мыши
        curses.curs_set(0)
        stdscr.keypad(True)

        #Пункты меню 
        self.menu_items = [
            "Find Game",
            "Wishlist",
            "Sales",
            "Main menu",
            "Exit"]
        
        current_item = 0

        # Получение размеров терминала 

        self.height, self.width = stdscr.getmaxyx()

        self.start_x = 0
        self.start_y = 0

        self.wishlist_menu = curses.newwin(self.width-90, self.height*3+1, self.start_y, self.start_x)

        self.wishlist_menu_panel = curses.panel.new_panel(self.wishlist_menu)

        while True:
            self.wishlist_menu.clear()
            self.wishlist_menu.border()

            self.title = "SPC"
            self.menu_title = "Wishlist Menu"
            self.wishlist_menu.addstr(2, self.width//2 - len(self.title)//2, self.title, curses.A_BOLD)
            self.wishlist_menu.addstr(3, self.width//2 - len(self.menu_title)//2, self.menu_title, curses.A_BOLD)
            # Инструкция
            self.wishlist_menu.addstr(self.height-2, 2, "↑↓: Choice | Enter: Select | F8: Main Menu | F10: Exit")
            #Разположение пунктов меню
            for idx, item in enumerate(self.menu_items):
                x = self.width//2 - len(item)//2 # Выравнивание x по центру
                y = self.height//2 - len(self.menu_items)//2 + idx # Выравнивание y по центру
                
                if idx == current_item:
                    # Выделенный пункт
                    self.wishlist_menu.addstr(y, x, f"> {item} <", curses.A_REVERSE)
                else:
                    # Невыделенный пункт 
                    self.wishlist_menu.addstr(y, x, f"  {item}  ")

            curses.panel.update_panels()
            stdscr.refresh()
            
            #ожидание нажатия клавши
            key = stdscr.getch()

            #управление
            if key == curses.KEY_UP:
                current_item = (current_item - 1) % len(self.menu_items)
            elif key == curses.KEY_DOWN:
                current_item = (current_item + 1) % len(self.menu_items)
            elif key == ord('\n') or key == ord('\r'):  # Enter
                return current_item
            elif key == curses.KEY_F10:
                quit()
    def Whishlist_menu(self, stdscr):
        curses.curs_set(0)
        self.choice = self.menu(stdscr)

        #Если выбран пункт Wishlist то запускать меню с вашим списком желаемого 
        if self.choice == 0:
            stdscr.clear()
            self.findGame = GameInfo()
        
        #Если выбран пункт Add the game to your wishlist, то запускать меню с добавлением игры в список желаемого 
        if self.choice == 1: 
            stdscr.clear()


        #Если выбран пункт Remove the game to your wishlist, то запускать меню с удалением игры из списка желаемого
        if self.choice == 2:
            stdscr.clear()
            # stdscr.addstr(10, 10, "Remove the game to your wishlist")
        
        # Если выбран пункт Sales, то запускеать меню со списком игр на которые сейчас скидка
        if self.choice == 3:
            stdscr.clear()
            # stdscr.addstr(10, 10, "Sales")
        
        if self.choice == 4: 
            stdscr.clear()
            # stdscr.addstr(10, 10, "Main menu")
            

        if self.choice == 5: 
            stdscr.clear()
            exit()
        
        stdscr.refresh()
        stdscr.getch()
    
    def find_game_information(self, stdscr, y, x, prompt, length):
        curses.curs_set(1)
        height, width = stdscr.getmaxyx()
        
        win_heigh = min(10, height - 4)
        win_width = min(50, width - 4)
        start_x = max(0, (width-19 - win_heigh) // 2)
        start_y = max(0, (height - win_heigh) // 2)

        find_game_menu = curses.newwin(win_heigh, win_width+19, start_y, start_x)
        find_game_menu.keypad(True)

        find_game_menu.border()
        title = "Game name or appID"
        find_game_menu.addstr(1, (win_width+19 - len(title)) // 2, title, curses.A_BOLD)
        find_game_menu.addstr(y, x, prompt)
        find_game_menu.refresh()

        curses.echo()
        try:
            find_game_input = find_game_menu.getstr(4, x + len(prompt), length).decode("utf-8")
        except curses.error:
            find_game_input = ""
        finally:
            curses.noecho()
            curses.curs_set(0)

        find_game_menu.clear()
        find_game_menu.refresh()

        return find_game_input.strip()
    def FindGameInput(self, stdscr):
        return self.find_game_information(stdscr, 4, 2, "Game:", 60)

    def FindGameMenu(self, stdscr):
        logger.remove()
        logger.add("logs/wishlist.log", rotation="500 MB")
        curses.curs_set(0)
        stdscr.clear()

        heigh, width = stdscr.getmaxyx()
        win_heigh = min(140, heigh -1)
        win_width = min(140, width -4 )
        start_x = max(0, (width-19 - win_width) // 2)
        start_y = max(0, (heigh - win_heigh) // 2)

        find_game_menu = curses.newwin(heigh-2, width, start_y, start_x)
        find_game_menu.keypad(True)

        while True:
            find_game_menu.clear()
            find_game_menu.border()

            GameName = self.FindGameInput(stdscr)

            if not GameName:
                logger.warning("Game not found!")
                continue
            try:
                game_info = GameInfo()

                # game_info.
                # 22.01.26 доделать меню с выводом информации о игре, а после задавать вопрос, добавлять ли игру в список желаемого или нет. 

                
            except Exception as e:
                # print(f"Error: {e}")
                logger.exception(f"ERROR: {e}")
                
            find_game_menu.refresh()

            key = find_game_menu.getch()

            if key == curses.KEY_F10:
                quit()

if __name__ == "__main__":
    WishlistMenu()