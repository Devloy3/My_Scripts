import sqlite3

conn = sqlite3.connect('../db/libros.db')
cursor = conn.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS libros(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               Titulo TEXT,
               Autor VARCHAR(50),
               Año INT,
               Total_paginas INT,
               Paginas_leidas INT,
               start_year INT);''')

cursor.execute('''
               CREATE TABLE IF NOT EXISTS libros_bibloteca(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               Titulo TEXT,
               fecha_finish DATE); ''' 
               )