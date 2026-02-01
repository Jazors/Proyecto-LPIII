import sqlite3

DB_URL = "./database/frontend_store.db"

def conectarDB():
    try:
      db = sqlite3.connect(DB_URL)
      db.row_factory = sqlite3.Row
      print("Conexión exitosa")
      
      return db

    except:
      print("Error")