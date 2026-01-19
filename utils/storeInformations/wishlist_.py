import sqlite3 

class Wishlist:
    def __init__(self):
        ...
    
    def wishilst_database(self):
        # Создание базы данных
        wishlist_db = sqlite3.connect("wishlist.db")

        cursor = wishlist_db.cursor()

        # Создание таблицы wishlist 
        cursor.execute("""
        CREATE TABLE wishlist(
                    appID integer NOT NULL,
                    name text NOT NULL,
                    type text NOT NULL,
                    price integer NOT NULL             
        )""")

        wishlist_db.commit()
        wishlist_db.close()
    
    

