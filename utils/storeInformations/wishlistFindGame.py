# from db_models import add_game, init_db
from .wishlist_ import *

import curses
import curses.panel 
import requests
import asyncio

class GameInfo:
    def __init__(self):
        find = curses.wrapper(self.FindMenu) # Запуск меню

    async def find_game_info(self, appid):

        try:
            url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
            self.responce = requests.get(url)
            self.json_game = self.responce.json()
        except Exception as e:
            return f"Error: {e}"
        
        #game_name
        self.game_name = self.json_game[f"{appid}"]["data"]["name"]
        #type(game/program)
        self.game_type = self.json_game[f"{appid}"]["data"]["type"]
        #steam_appid
        self.steam_appid = self.json_game[f"{appid}"]["data"]["steam_appid"]

        #Price
        self.is_free = self.json_game[f"{appid}"]["data"]["is_free"]
        if self.is_free == True:
            self.is_free == "Free"
        if self.is_free == False:
            self.is_free = self.json_game[f"{appid}"]["data"]["price_overview"]["initial_formatted"]
            if self.is_free == "":
                self.is_free = self.json_game[f"{appid}"]["data"]["price_overview"]["final_formatted"]
            if self.is_free != None:
                self.is_free = f"[s]{self.json_game[f"{appid}"]["data"]["price_overview"]["initial_formatted"]}[/s]" + " " + self.json_game[f"{appid}"]["data"]["price_overview"]["final_formatted"]

        # Добавление информации о игре в базу данных
        try:
            await Wishlist.AddGame(
                game_name=self.game_name,
                game_type=self.game_type,
                app_id=appid,
                price=0,
                discount_price=0
            )
        except Exception as e:
            print("error while adding game to db: {}", e)


    def find_appid(self, appName):
        try:
            appid_url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
            appid_url_responce = requests.get(appid_url)

            self.data = appid_url_responce.json()

            for self.game in self.data["applist"]["apps"]:
                if self.game["name"].lower() == appName.lower():
                    return self.game["appid"]
        except:
            print("Game is not found... =(")

#+----------------------------------+
#|               MENU               |
#+----------------------------------+

    # Меню ввода
    def InputMenu(self, stdscr, y, x, prompt, length):
        curses.curs_set(1) # Включить курсор
        stdscr.keypad(True)

        height, width = stdscr.getmaxyx() # Получить размеры терминала
        
        win_height = min(10, height - 4) # Высота окна 
        win_width = min(50, width - 4) # Ширина окна
        start_x = max(0, (width-19 - win_width) // 2) # Начало координат окна по x
        start_y = max(0, (height - win_height) // 2) # Начало координат окна по y
        
        # Создание окна для ввода
        find_menu = curses.newwin(win_height, win_width+19, start_y, start_x)
        find_menu.keypad(True)
        
        # Отрисовка окна
        find_menu.border() # Рамка окна
        title = "Search"  # Заголовок окна ввода 
        find_menu.addstr(1, (win_width+19 - len(title)) // 2, title, curses.A_BOLD) # Добавление заголовка окна(центрированно)
        find_menu.addstr(y, x, prompt)
        find_menu.refresh()
        
        # Ввод данных
        curses.echo() # Разрешить ввод
        try:
            find_input = find_menu.getstr(4, x + len(prompt), length).decode('utf-8')
        except curses.error:
            find_input = ""
        finally:
            curses.noecho() # Запретить ввод
            curses.curs_set(0) # Отключить курсор
        
        #После ввода, очищать экран 
        find_menu.clear() 
        find_menu.refresh()
        
        return find_input.strip()
    
    # Функция возвращает введенный текст 
    def GameName(self, stdscr):
        return self.InputMenu(stdscr, 4, 2, "Game: ", 60)
    
    # Поиск и вывод информации об игре(appid, название, стоимость, стоимость со скидкой, итд). 
    def FindMenu(self, stdscr):
        curses.curs_set(0)
        stdscr.clear()

        height, width = stdscr.getmaxyx()
        win_height = min(140, height - 1)
        win_width = min(140, width - 4)
        start_x = max(0, (width-19 - win_width) // 2)
        start_y = max(0, (height - win_height) // 2)

        find_info_menu = curses.newwin(height-2, width, start_y, start_x)
        find_info_menu.keypad(True)

        while True:
            find_info_menu.clear()
            find_info_menu.border()

            appName = self.GameName(stdscr) 
            

            if not appName:
                continue
            try:
                # Поиск appid по названию игры
                appid = self.find_appid(appName=appName) # Получение appid 
                find_game = asyncio.run(self.find_game_info(appid=appid)) # Получение информации об игре по полученному appid 
                
            except Exception as e:
                stdscr.clear()
                find_info_menu.addstr(10, 10, f"Error: {e}")
                stdscr.refresh()

            find_info_menu.refresh()

            key = find_info_menu.getch()

# +-------------------------------------+
# |               HOTKEYS               |
# +-------------------------------------+         
            if key == curses.KEY_F10:
                quit()


if __name__ == "__main__":
    run = GameInfo()