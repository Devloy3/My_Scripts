import sqlite3
from datetime import date

conn = sqlite3.connect('./db/libros.db')
cursor = conn.cursor()

def añadir_libro_para_leer(Titulo, Autor, Año,Total_paginas):
    cursor.execute('INSERT INTO libros (Titulo, Autor, Año, Total_paginas) VALUES (?, ?, ?, ?)', (Titulo, Autor, Año, Total_paginas))
    conn.commit()
    cursor.close()
    print("Libro añadido correctamente.")

def mostrar_libros_que_quedan_por_leer():
    cursor.execute('SELECT * FROM libros WHERE Paginas_leidas = 0')
    libros = cursor.fetchall()
    if libros:
        print("Libros que quedan por leer: \n")
        for libro in libros:
            print(f"Título: {libro[1]}, Autor: {libro[2]}, Año: {libro[3]}, Total Páginas: {libro[4]}")
    else:
        print("No hay libros que quedan por leer.")
    conn.close()


def actualizar_paginas_leidas(id, nuevas_paginas):
    cursor.execute('UPDATE libros SET Paginas_leidas = ? WHERE id=?',(nuevas_paginas, id))
    conn.commit()
    cursor.close()

def empezar_libro(Titulo,nuevas_paginas,start_year):
    cursor.execute('UPDATE libros SET Paginas_leidas = ?, start_year = ? WHERE Titulo = ?', (nuevas_paginas, start_year, Titulo))
    conn.commit()
    if cursor.rowcount > 0:
        print(f"Se ha empezado a leer el libro '{Titulo}'.")
    else:
        print(f"No se encontró el libro '{Titulo}' para empezar.")
    cursor.close()

def cuanto_me_falta_para_terminar(Titulo):
    cursor.execute('SELECT Total_paginas - Paginas_leidas AS paginas_restantes FROM libros WHERE Titulo = ?', (Titulo,))
    libro = cursor.fetchone()
    if libro:
        paginas_restantes = libro[0]
        if paginas_restantes > 0:
            print(f"Te queda para terminar el libro: {paginas_restantes} paginas \n")
        else:
            print("Ya se ha terminado el libro \n")
    else:
        print(f"No se encontró el libro")
    cursor.close()

def mostrar_libros():
    cursor.execute('SELECT * FROM libros')
    libros = cursor.fetchall()
    if libros:
        print("Lista de libros:")
        for libro in libros:
            print(f"ID:{libro[0]} Título: {libro[1]}, Autor: {libro[2]},  Año: {libro[3]}, Total Páginas: {libro[4]}")
    else:
        print("No hay libros en la base de datos.")

def mostrar_libros_bibloteca():
    cursor.execute('SELECT * FROM libros_bibloteca')
    bibloteca = cursor.fetchall()
    
    for libro in bibloteca:
        print(f'ID: {libro[0]} Título: {libro[1]}, Fecha de entrega: {libro[3]}')

def mostrar_dias_libro(id):
  cursor.execute('SELECT fecha_finish FROM libros_bibloteca WHERE id=?',(id,))
  libro = cursor.fetchone()
    
  if libro:
      
      resultado = libro[0]
      fecha_finish = date.fromisoformat(resultado)
      actual = date.today()
      diferencia = fecha_finish - actual 
        
      if diferencia.days == 0:
           print("Se te acabaron los dias")
      elif diferencia.days < 0:
           print(f"Tienes un retraso de {-diferencia.days} dias")
      else:
          print(f"Te quedan {diferencia.days} dias para devolverlo")
  else:
     print('No esta en la base de datos')

def main():
    while True:
        print("\n <--- Menú de Gestión de Libros---> \n")
        print("1. Añadir libro para leer")
        print("2. Mostrar libros que quedan por leer")
        print("3. Actualizar páginas leídas de un libro")
        print("4. Empezar a leer un libro")
        print("5. Consultar cuánto falta para terminar un libro")
        print("6. Consultar todos los libros que hay en la base de datos ")
        print("7. Consultar todos los libros de la biblo ")
        print("8. Consultar cuantos dias tengo de dias sobre un libro ")
        print("9. Salir \n")
        
        opcion = input("Selecciona una opción: ")   

        if opcion == '1':
            Titulo = input("Introduce el título del libro: ")
            Autor = input("Introduce el autor del libro: ")
            Año = input("Introduce el año de publicación: ")
            Total_paginas = int(input("Introduce el total de páginas del libro: "))
            añadir_libro_para_leer(Titulo, Autor, Año, Total_paginas)
        elif opcion == '2':
            mostrar_libros_que_quedan_por_leer()
        elif opcion == '3':
            Titulo = input("Introduce el id del libro: ")
            nuevas_paginas = int(input("Introduce la pagina en la cual estas: "))
            actualizar_paginas_leidas(Titulo, nuevas_paginas)
        elif opcion == '4':
            Titulo = input("Introduce el título del libro: ").strip()
            nuevas_paginas = int(input("Introduce el número de páginas leidas: "))
            start_year = input("Introduce el año en el que lo has empezado a leer: ")
            empezar_libro(Titulo, nuevas_paginas, start_year)
        elif opcion == '5':
            Titulo = input("Introduce el Titulo del libro: ").strip()
            cuanto_me_falta_para_terminar(Titulo)
        elif opcion == '6':
            mostrar_libros()
        elif opcion == '7':
            mostrar_libros_bibloteca()
        elif opcion == '8':
            id = int(input("Introduce el id del libro: "))
            mostrar_dias_libro(id)
        elif opcion == '9':
            break


main()