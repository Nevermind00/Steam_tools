import sqlite3 
from loguru import logger

# class Wishlist:
#     def __init__(self):
#         self.wishlist_db = None
#         self.cursor = None
#         self.wishlist_database()  # Автоинициализация БД
    
def init_wishlist_db():
        # Создание базы данных
    global wishlist_db
    wishlist_db = sqlite3.connect("wishlist.db")

        
    # cursor = wishlist_db.cursor()

        # Создание таблицы wishlist 
    wishlist_db.cursor.execute("""
        CREATE TABLE IF NOT EXISTS wishlist(
                       id INTEGER PRIMARY KEY,
                       game_name TEXT NOT NULL,
                       game_type TEXT NOT NULL,
                       app_id BIGINT NOT NULL,
                       price INTEGER NOT NULL,
                       discount_price INT NULL
        )""")

    wishlist_db.commit()

    #функции добавления и удаления игры из бд
def AddGame(
                game_name: str, 
                game_type: str, 
                app_id: int, 
                price: int, 
                discount_price: int = None):
    logger.remove()
    logger.add("logs/wishlist.log", rotation="500 MB")

    try:
        wishlist_db.cursor.execute("INSERT INTO wishlists (game_name, game_type, app_id, price, discount_price) VALUES (?, ?, ?, ?, ?)",
            (game_name, game_type, app_id, price, discount_price if discount_price else "")
            )
        wishlist_db.commit()

        logger.success(f"Game: {game_name}({app_id}) has been added to the wishlist ✅")
    except sqlite3.Error as e:
        wishlist_db.rollback()



        
    def RemoveGame():
        ...

if __name__ == "__main__":
    ...