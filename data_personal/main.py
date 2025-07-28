from models.tablas import trabajo
import sqlite3
from reportlab.platypus import SimpleDocTemplate,Paragraph,Image,Spacer
from reportlab.lib.styles import getSampleStyleSheet

conn = sqlite3.connect('./datos/datos_personales.db')
cursor = conn.cursor()

def buscar_contactos(Nombre):
     
    cursor.execute("SELECT id,Nombre,Apellidos,Año,Email,Telefono FROM contactos WHERE Nombre=?",(Nombre,))
    contacto = cursor.fetchall()
    if contacto:
        for id, nombre, apellido, nacimiento, email, telfono in contacto:
         print(f"\n ID:{id}, Nombre: {nombre}, Apellido: {apellido}, Año de Nacimineto: {nacimiento}, Email:{email}, Telefono: {telfono}")
    else:
        print("\n No hay nada en la base de datos")


def crear_archivo_vcf(Nombre,Apellido):
    cursor.execute(f"SELECT Nombre,Apellidos,Telefono FROM contactos WHERE Nombre=? AND Apellidos =?",(Nombre,Apellido))
    contacto = cursor.fetchone()
    if contacto:
        nombre,apellido,Telefono = contacto
        vcf = f"""
        BEGIN:VCARD
        VERSION:3.0
        FN:{nombre}-{apellido}
        TEL: {Telefono}
        END:VCARD
        """
        with open(f"../vcf/{nombre}{apellido}.vcf", 'w') as fs:
            fs.write(vcf)
        print(f"\n Archivo creado de {nombre}-{apellido}")
    else:
        print("resultado no encontrado")

def crear_contacto_simple(Nombre,Apellido,Telefono):
    cursor.execute("INSERT INTO contactos(Nombre,Apellidos,Telefono) VALUES (?,?,?)", (Nombre,Apellido,Telefono))
    conn.commit()

def crear_contacto_todo(Nombre,Apellido,Telefono,Año,Email,Pais):
    cursor.execute("INSERT INTO contactos(Nombre,Apellidos,Telefono,Año,Email,Telefono_Pais) VALUES (?,?,?,?,?,?)", (Nombre,Apellido,Telefono,Año,Email,Pais))
    conn.commit()

def eliminar_contacto(id):
    cursor.execute("DELETE FROM contactos WHERE id=?", (id,))
    conn.commit()
    
     
def pdf_trabajo(car):
   
    doc = SimpleDocTemplate('../pdf/Trabajo.pdf')
    estilos = getSampleStyleSheet()
    datos = trabajo.all()[0]
    contenido = []
	
    contenido.append(Paragraph("Datos de Trabajo", estilos["Heading1"]))
	
    contenido.append(Spacer(0,30))
    
    for clave,valor in datos.items():
        Texto = f"<b>{clave}</b>: {valor}"
        contenido.append(Paragraph(Texto, estilos["Normal"]))

    contenido.append(Spacer(0,30))    
    contenido.append(Image("./img/DNI(1).jpg", width=398.88, height=249.96))
    contenido.append(Spacer(0,50))
    contenido.append(Image("./img/DNI(2).jpg", width=398.88, height=249.96))
    contenido.append(Spacer(0,50))
    
    if car == 1:
        contenido.append(Image("./img/Carnet(1).jpg", width=398.88, height=249.96))
        contenido.append(Spacer(0,50))
        contenido.append(Image("./img/Carnet(2).jpg", width=398.88, height=249.96))
    elif car == 2:
        pass
    
    doc.build(contenido)

def pdf_datos(Dni,Carnet):
    
    c = SimpleDocTemplate('../pdf/DNI_Carnet_Passaporte.pdf')
    contenido = []
    
    if Dni == 1:
        contenido.append(Image("./img/DNI(1).jpg", width=398.88, height=249.96))
        contenido.append(Spacer(0,50))
        contenido.append(Image("./img/DNI(2).jpg", width=398.88, height=249.96))
    else:
        pass

    if Carnet == 1:
        contenido.append(Image("./img/Carnet(1).jpg", width=398.88, height=249.96))
        contenido.append(Spacer(0,50))
        contenido.append(Image("./img/Carnet(2).jpg", width=398.88, height=249.96))
    else:
        pass
    
    c.build(contenido)

def modificar_datos_trabajo(DNI,SS,Bancaria):
    trabajo.update({
                    'DNI':DNI,
                    'Seguridad Social':SS, 
                    'Cuenta Bancaria': Bancaria 
                    },
                    doc_ids=[1])
     

def añdir_cuentas(cuenta,usuario,contrasenya):
    cursor.execute("INSERT INTO cuentas (cuenta,usuario,contrasenya) VALUES (?,?,?)", (cuenta,usuario,contrasenya))
    conn.commit()

def buscar_cuenta(cuenta):
    
    cursor.execute("SELECT usuario,contrasenya FROM cuentas WHERE cuenta=?", (cuenta,))
    resultado = cursor.fetchone()
    
    if resultado:
        usuario = resultado[0]
        contrasenya = resultado[1]
        print(f"\n Usuario: {usuario} Contraseña: {contrasenya}")
    else:
        print("Cuenta no encontrada")

def modificar_cuenta_usuario(cuenta,usuario):
    cursor.execute("UPDATE cuentas SET usuario=? WHERE cuenta=? ", (usuario,cuenta))
    conn.commit()

def modificar_cuenta_contrasenya(cuenta,contrasenya):
    cursor.execute("UPDATE cuentas SET contrasenya=? WHERE cuenta=? ",(contrasenya,cuenta))
    conn.commit()
         


def menu():
        while True:

            print("\n <-- Gestion de Contactos --> \n")
            print("1.Buscar Contactos")
            print("2.Crear contacto simple")
            print("3.Crear contacto con todos los datos")
            print("4.Eliminar contacto")
            print("5.Pasar contacto a Archivo.vcf \n")
            print("<-- Gestion de Trabajo --> \n")
            print("6.Modificar datos de Trabajo")
            print("7.Hacer PDF de trabajo")
            print("8.Crear PDF de DNI, Passaporte o Carnet \n")
            print("<-- Gestion de cuentas --> \n")
            print("9.Añadir Cuenta")
            print("10.Buscar una Cuenta")
            print("11.Modificar el usuario de una cuenta")
            print("12.Modificar la contrasenya de una cuenta")
            print("13.Salir \n")
            
            opcion = int(input("Que hacemos?"))

            if opcion == 1:
                    Nombre = input("Nombre del Contacto:").strip()
                    buscar_contactos(Nombre)
            elif opcion == 2:
                    Nombre = input("Nombre:")
                    Apellido = input("Apellido:")
                    Telefono = int(input("Telefono:"))
                    crear_contacto_simple(Nombre,Apellido,Telefono)
            elif opcion == 3:
                    Nombre = input("Nombre:")
                    Apellido = input("Apellido:")
                    Telefono = int(input("Telefono:"))
                    Año = input("Introduce el Año de Nacimiento asi 0000-00-00:")
                    Email = input("Email:")
                    Pais = input("Tres de letras de que pais es el Telfono:")
                    crear_contacto_todo(Nombre,Apellido,Telefono,Año,Email,Pais)
            elif opcion == 4:
                    id = int(input("id del contacto:"))
                    eliminar_contacto(id)
            elif opcion == 5:
                    Nombre = input("Nombre del contacto:").strip()
                    Apellido = input("Apellido del Contacto:").strip()
                    crear_archivo_vcf(Nombre,Apellido)
            elif opcion == 6:
                    DNI = input("Nuevo DNI:")
                    SS = input("Nuevo Numero de la SS:")
                    Bancaria = input("Nueva Cuenta Bancaria: ")
                    modificar_datos_trabajo(DNI,SS,Bancaria)
            elif opcion == 7:
                    print("Quieres incluir el carnet de conducir? (SI/NO)")
                    car = int(input("1.SI / 2.NO"))
                    pdf_trabajo(car)
            elif opcion == 8:
                    Dni = int(input("Quieres incluir el DNI en el pdf? 1.SI 2.NO"))
                    Carnet = int(input("Quieres incluir el Carnet de Conducir? 1.SI 2.NO"))
                    pdf_datos(Dni,Carnet)
            elif opcion == 9:
                    cuenta = input("Que tipo de cuenta es?")
                    usuario = input("Usuario:")
                    contrasenya = input("Contraseña:")
                    añdir_cuentas(cuenta,usuario,contrasenya)
            elif opcion == 10:
                    cuenta = input("Que cuenta quieres buscar?").strip()
                    buscar_cuenta(cuenta)
            elif opcion == 11:
                    cuenta = input("Que cuenta quieres modificar?").strip()
                    usuario = input("Nuevo Usuario:")
                    modificar_cuenta_usuario(cuenta,usuario)
            elif opcion == 12:
                    cuenta = input("Que cuenta quieres modificar?").strip()
                    contrasenya = input("Nueva Contrasenya:")
                    modificar_cuenta_contrasenya(cuenta,contrasenya)
            elif opcion == 13:
                cursor.close()
                break
            
                 
menu()










    

        

       



