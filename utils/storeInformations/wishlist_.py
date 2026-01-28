import sqlite3 

class Wishlist:
    def __init__(self):
        ...
    
    def wishilst_database(self):
        # Создание базы данных
        self.wishlist_db = sqlite3.connect("wishlist.db")


        global cursor
        cursor = self.wishlist_db.cursor()

        # Создание таблицы wishlist 
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS wishlist(
                    appID integer NOT NULL,
                    name text NOT NULL,
                    type text NOT NULL,
                    price integer NOT NULL             
        )""")

        self.wishlist_db.commit()
        # self.wishlist_db.close()
    

    #функции добавления и удаления игры из бд
    def AddGame(self, game_name: str, game_type: str, app_id: int, price: int, discount_price: int = None):
        cursor.execute("INSERT INTO wishlists (game_name, game_type, app_id, price, discount_price) VALUES (?, ?, ?, ?, ?)",
        (game_name, game_type, app_id, price, discount_price if discount_price else "")
        )
        self.wishlist_db.commit()


        
    def RemoveGame():
        ...

if __name__ == "__main__":
    run = Wishlist()