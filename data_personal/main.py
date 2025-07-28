from models.models import trabajo
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
         print(f"\n ID:{id}, Name: {nombre}, Last Name: {apellido}, Birth Date: {nacimiento}, Email:{email}, Phone: {telfono}")
    else:
        print("\n Not found")


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
        print(f"\n File created from {nombre}-{apellido}")
    else:
        print("Not found")

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

def insertar_datos_trabajo(Nombre,Apellidos,DNI,SS,Cuenta_Bancaria):
     trabajo.insert({
          'Nombre': Nombre,
          'Apellidos': Apellidos,
          'DNI': DNI,
          'Seguridad Social': SS,
          'Cuenta Bancaria': Cuenta_Bancaria
     })

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
        print(f"\n User: {usuario} Password: {contrasenya}")
    else:
        print("Account not found")

def modificar_cuenta_usuario(cuenta,usuario):
    cursor.execute("UPDATE cuentas SET usuario=? WHERE cuenta=? ", (usuario,cuenta))
    conn.commit()

def modificar_cuenta_contrasenya(cuenta,contrasenya):
    cursor.execute("UPDATE cuentas SET contrasenya=? WHERE cuenta=? ",(contrasenya,cuenta))
    conn.commit()
         


def menu():
        while True:

            print("\n <-- Contact Management --> \n")
            print("1.Search Contacts")
            print("2.Create Simple Contact")
            print("3.Create Contact with All Data")
            print("4.Delete Contact")
            print("5.Transfer Contact to File.vcf \n")
            print("<-- Work Management --> \n")
            print("6. Insert Work Data")
            print("7. Modify Work Data")
            print("8. Create Work PDF")
            print("9. Create PDF of ID Card, Passport, or License \n")
            print("<-- Account Management --> \n")
            print("10.Add Account")
            print("11.Search for an Account")
            print("12.Modify an account user")
            print("13.Modify an account password")
            print("14.Exit \n")
            
            opcion = int(input("What we do?"))

            if opcion == 1:
                    Nombre = input("Contact Name:").strip()
                    buscar_contactos(Nombre)
            elif opcion == 2:
                    Nombre = input("Name:")
                    Apellido = input("Last Name:")
                    Telefono = int(input("Phone:"))
                    crear_contacto_simple(Nombre,Apellido,Telefono)
            elif opcion == 3:
                    Nombre = input("Name:")
                    Apellido = input("Last Name:")
                    Telefono = int(input("Phone:"))
                    Año = input("Enter your year of birth as 0000-00-00:")
                    Email = input("Email:")
                    Pais = input("Three letters from which country is the phone number:")
                    crear_contacto_todo(Nombre,Apellido,Telefono,Año,Email,Pais)
            elif opcion == 4:
                    id = int(input("ID contact:"))
                    eliminar_contacto(id)
            elif opcion == 5:
                    Nombre = input("Contact Name:").strip()
                    Apellido = input("Last Name Contact:").strip()
                    crear_archivo_vcf(Nombre,Apellido)
            elif opcion == 6:
                    Nombre = input("Name:").strip()
                    Apellidos = input("Last Name:").strip()
                    DNI = input("National Identity Card:").strip()
                    SS = input("Social Security Number:").strip()
                    Cuenta_Bancaria = input("Account Bank:").strip()
                    insertar_datos_trabajo(Nombre,Apellidos,DNI,SS,Cuenta_Bancaria)
            elif opcion == 7:
                    DNI = input(" New National Identity Card:")
                    SS = input("New Social Security Number:")
                    Bancaria = input("New Bank Account: ")
                    modificar_datos_trabajo(DNI,SS,Bancaria)
            elif opcion == 8:
                    print("Do you want to include your driver card?")
                    car = int(input("1.YES / 2.NO"))
                    pdf_trabajo(car)
            elif opcion == 9:
                    Dni = int(input("Do you want to include your National Identity Card in pdf? 1.YES 2.NO"))
                    Carnet = int(input("Do you want to include your driver card? 1.YES 2.NO"))
                    pdf_datos(Dni,Carnet)
            elif opcion == 10:
                    cuenta = input("What type of account is it?")
                    usuario = input("User:")
                    contrasenya = input("Password:")
                    añdir_cuentas(cuenta,usuario,contrasenya)
            elif opcion == 11:
                    cuenta = input("Which account do you want to search for?").strip()
                    buscar_cuenta(cuenta)
            elif opcion == 12:
                    cuenta = input("Which account do you want to modify?").strip()
                    usuario = input("New User:")
                    modificar_cuenta_usuario(cuenta,usuario)
            elif opcion == 13:
                    cuenta = input("Which account do you want to modify?").strip()
                    contrasenya = input("Nueva Contrasenya:")
                    modificar_cuenta_contrasenya(cuenta,contrasenya)
            elif opcion == 14:
                cursor.close()
                break
            
                 
menu()










    

        

       



