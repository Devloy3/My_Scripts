import sqlite3
from datetime import date

conn = sqlite3.connect('./db/libros.db')
cursor = conn.cursor()

def añadir_libro_para_leer(Titulo, Autor, Año,Total_paginas):
    cursor.execute('INSERT INTO libros (Titulo, Autor, Año, Total_paginas) VALUES (?, ?, ?, ?)', (Titulo, Autor, Año, Total_paginas))
    conn.commit()
    cursor.close()
    print("Book added successfully.")

def mostrar_libros_que_quedan_por_leer():
    cursor.execute('SELECT * FROM libros WHERE Paginas_leidas = 0')
    libros = cursor.fetchall()
    if libros:
        print("Books still to read: \n")
        for libro in libros:
            print(f"Title: {libro[1]}, Author: {libro[2]}, Year: {libro[3]}, Total Pages: {libro[4]}")
    else:
        print("There are no more books to read.")
    conn.close()


def actualizar_paginas_leidas(id, nuevas_paginas):
    cursor.execute('UPDATE libros SET Paginas_leidas = ? WHERE id=?',(nuevas_paginas, id))
    conn.commit()
    cursor.close()

def empezar_libro(Titulo,nuevas_paginas,start_year):
    cursor.execute('UPDATE libros SET Paginas_leidas = ?, start_year = ? WHERE Titulo = ?', (nuevas_paginas, start_year, Titulo))
    conn.commit()
    if cursor.rowcount > 0:
        print(f"The book has started to be read {Titulo}.")
    else:
        print(f"The book to start with was not found.{Titulo}")
    cursor.close()

def cuanto_me_falta_para_terminar(Titulo):
    cursor.execute('SELECT Total_paginas - Paginas_leidas AS paginas_restantes FROM libros WHERE Titulo = ?', (Titulo,))
    libro = cursor.fetchone()
    if libro:
        paginas_restantes = libro[0]
        if paginas_restantes > 0:
            print(f"You have left to finish the book: {paginas_restantes} pages \n")
        else:
            print("The book is finished \n")
    else:
        print(f"Not found the book")
    cursor.close()

def mostrar_libros():
    cursor.execute('SELECT * FROM libros')
    libros = cursor.fetchall()
    if libros:
        print("Book List:")
        for libro in libros:
            print(f"ID:{libro[0]} Title: {libro[1]}, Author: {libro[2]},  Year: {libro[3]}, Total Pages: {libro[4]}")
    else:
        print("No books found in the database.")

def mostrar_libros_bibloteca():
    cursor.execute('SELECT * FROM libros_bibloteca')
    bibloteca = cursor.fetchall()
    
    for libro in bibloteca:
        print(f'ID: {libro[0]} Title: {libro[1]}, Delivery Date: {libro[3]}')

def mostrar_dias_libro(id):
  cursor.execute('SELECT fecha_finish FROM libros_bibloteca WHERE id=?',(id,))
  libro = cursor.fetchone()
    
  if libro:
      
      resultado = libro[0]
      fecha_finish = date.fromisoformat(resultado)
      actual = date.today()
      diferencia = fecha_finish - actual 
        
      if diferencia.days == 0:
           print("The days are over")
      elif diferencia.days < 0:
           print(f"You are {-diferencia.days} days late")
      else:
          print(f"You have {diferencia.days} days left to return it")
  else:
     print('Not found in database')

def main():
    while True:
        
        print("\n <--- Book Management Menu---> \n")
        print("1. Add book to read")
        print("2. Show books left to read")
        print("3. Update pages read in a book")
        print("4. Start reading a book")
        print("5. Check how much is left to finish a book")
        print("6. Check all books in the database")
        print("7. Check all books in the library")
        print("8. Check how many days I have left on a book")
        print("9. Exit \n")
        
        opcion = input("Select an option: ")   

        if opcion == '1':
            Titulo = input("Enter the title of the book: ")
            Autor = input("Enter the autor of the book: ")
            Año = input("Enter the year of the book: ")
            Total_paginas = int(input("Enter the total pages of the book: "))
            añadir_libro_para_leer(Titulo, Autor, Año, Total_paginas)
        elif opcion == '2':
            mostrar_libros_que_quedan_por_leer()
        elif opcion == '3':
            Titulo = input("Enter id of the book: ")
            nuevas_paginas = int(input("Enter the page you are on: "))
            actualizar_paginas_leidas(Titulo, nuevas_paginas)
        elif opcion == '4':
            Titulo = input("Enter the title of the book: ").strip()
            nuevas_paginas = int(input("Enter the page you are on: "))
            start_year = input("Enter the year in which you started reading the book: ")
            empezar_libro(Titulo, nuevas_paginas, start_year)
        elif opcion == '5':
            Titulo = input("Enter the title of the book: ").strip()
            cuanto_me_falta_para_terminar(Titulo)
        elif opcion == '6':
            mostrar_libros()
        elif opcion == '7':
            mostrar_libros_bibloteca()
        elif opcion == '8':
            id = int(input("Enter id of the book: "))
            mostrar_dias_libro(id)
        elif opcion == '9':
            break


main()