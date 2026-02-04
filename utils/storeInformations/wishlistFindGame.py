# from .wishlist_ import *    #Database
import curses               
import curses.panel         
import requests     
import asyncio      
from loguru import logger   

import requests

from utils.storeInformations.wishlist_ import Wishlist


class GameInfo:
    def __init__(self):
        logger.remove()
        logger.add("logs/wishlist.log", rotation="500 MB")
        logger.info("WishlistFindGame Running!")
        find = curses.wrapper(self.FindMenu) # Запуск меню

    async def find_game_info(self, appid):
        logger.remove()
        logger.add("logs/wishlist.log", rotation="500 MB")
        try:
            url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
            self.responce = requests.get(url)
            self.json_game = self.responce.json()
        except Exception as e:
            logger.exception(f"Error(find_game_info): {e}")
        
        # GAME INFO
        self.game_name = self.json_game[f"{appid}"]["data"]["name"] #GAME_NAME
        self.game_type = self.json_game[f"{appid}"]["data"]["type"] #type(game/program)
        self.steam_appid = self.json_game[f"{appid}"]["data"]["steam_appid"] #steam_appid
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
        self.game_link = ""

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
            logger.exception(f"ERROR(find_game_info): {e}")






    # async def find_game_info(self, appid):
    #     logger.remove()
    #     logger.add("logs/wishlist.log", rotation="500 MB")
        
    #     try:
    #         # ✅ Исправлен URL: убраны лишние пробелы
    #         url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    #         response = requests.get(url, timeout=10)
    #         response.raise_for_status()
            
    #         json_game = response.json()
    #         appid_str = str(appid)
            
    #         # ✅ Проверка успешности ответа от Steam
    #         if not json_game.get(appid_str, {}).get('success'):
    #             logger.error(f"Steam API вернул ошибку для AppID {appid}")
    #             return
            
    #         game_data = json_game[appid_str]['data']
            
    #         # ✅ Извлечение данных
    #         game_name = game_data.get('name', 'Unknown')
    #         game_type = game_data.get('type', 'unknown')
    #         is_free = game_data.get('is_free', False)
            
    #         # ✅ Корректная обработка цены
    #         if is_free:
    #             price = 0
    #             discount_price = 0
    #         else:
    #             price_overview = game_data.get('price_overview', {})
    #             # Steam возвращает цены в центах — конвертируем в рубли/доллары
    #             price = price_overview.get('initial', 0) // 100
    #             final = price_overview.get('final', 0) // 100
    #             discount_price = final if final < price else None
            
    #         # ✅ Вызов БЕЗ await (метод синхронный!)
    #         wishlist = Wishlist()  # Создаём экземпляр
    #         wishlist.AddGame(
    #             game_name=game_name,
    #             game_type=game_type,
    #             app_id=appid,
    #             price=price,
    #             discount_price=discount_price
    #         )
            
    #     except Exception as e:
    #         logger.exception(f"Ошибка в find_game_info (AppID: {appid}): {e}")







    def find_appid(self, appName):
        logger.remove()
        logger.add("logs/wishlist.log", rotation="500 MB")
        try:

# FIXME Не работает API по поиску APPID(код 404)
# Valve закрали доступ к (https://api.steampowered.com/ISteamApps/GetAppList/v2/) списку игр(возможно временно). Если снова дадут доступ к данному API, нужно будет захешировать полученный результат!
#--------------------------------------------------------------------------------------------
            
            # appid_url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
            # appid_url_responce = requests.get(appid_url)

            # self.data = appid_url_responce.json()

            # for self.game in self.data["applist"]["apps"]:
            #     if self.game["name"].lower() == appName.lower():
            #         return self.game["appid"]



#--------------------------------------------------------------------------------------------
            ...
        except Exception as e:
            logger.exception(f"ERROR: {e}")


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
        return self.InputMenu(stdscr, 4, 2, "NAME/APPID: ", 60)
    
    # Поиск и вывод информации об игре(appid, название, стоимость, стоимость со скидкой, итд). 
    def FindMenu(self, stdscr):
        logger.remove()
        logger.add("logs/wishlist.log", rotation="500 MB")
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
            logger.success(f"AppName - {appName}") 
            
            if not appName:
                logger.warning("Game not found!")
                continue
            try:
                # if appName == int:
                find_game = asyncio.run(self.find_game_info(appid=730)) # Получение
                # Поиск appid по названию игры
                # appid = self.find_appid(appName=appName) # Получение appid 
                # find_game = asyncio.run(self.find_game_info(appid=appid)) # Получение информации об игре по полученному appid 
            
            except Exception as e:
                stdscr.clear()
                logger.exception("ERROR(FindMenu): {e}")
                stdscr.refresh()

            find_info_menu.refresh()

            key = find_info_menu.getch()

# +-------------------------------------+
# |               HOTKEYS               |
# +-------------------------------------+         
            #  exit
            if key == curses.KEY_F10:
                exit()


if __name__ == "__main__":
    ...
