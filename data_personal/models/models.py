from tinydb import TinyDB
import sqlite3

conn = sqlite3.connect('../datos/datos_personales.db')
cursor = conn.cursor()

db = TinyDB('../datos/datos_personales.json')
trabajo = db.table('trabajo')

cursor.execute('''
               CREATE TABLE IF NOT EXISTS contactos(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               Nombre TEXT,
               Apellidos TEXT,
               Año DATE,
               Email VARCHAR(100),
               Telefono INT,
               Telefono_pais CHAR(3)''' )

cursor.execute('''
               CREATE TABLE IF NOT EXISTS cuentas(
               Cuenta VARCHAR(100),
               usuario TEXT,
               contrasenya TEXT)
               ''')