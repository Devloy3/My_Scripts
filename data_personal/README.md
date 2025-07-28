# App Personal_data

This app is entirely local.

## Installation 

1. Frameworks 

```
pip install tinydb
pip install reportlab
```
2. Start the database module 

```
python3 models.py
```
3. Place the images of your ID card and driver's license in this section.

```
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
    contenido.append(Image("./img/DNI(1).jpg", width=398.88, height=249.96)) <----HERE(Identity National Card(front))
    contenido.append(Spacer(0,50))
    contenido.append(Image("./img/DNI(2).jpg", width=398.88, height=249.96)) <----HER(Identity National Card(back))
    contenido.append(Spacer(0,50))
    
    if car == 1:
        contenido.append(Image("./img/Carnet(1).jpg", width=398.88, height=249.96))<----HERE(Card Driver(front))
        contenido.append(Spacer(0,50))
        contenido.append(Image("./img/Carnet(2).jpg", width=398.88, height=249.96))<----HERE(Card Driver(back))
    elif car == 2:
        pass
    
    doc.build(contenido)

def pdf_datos(Dni,Carnet):
    
    c = SimpleDocTemplate('../pdf/DNI_Carnet_Passaporte.pdf')
    contenido = []
    
    if Dni == 1:
        contenido.append(Image("./img/DNI(1).jpg", width=398.88, height=249.96))<----HERE(Identity National Card(front))
        contenido.append(Spacer(0,50))
        contenido.append(Image("./img/DNI(2).jpg", width=398.88, height=249.96))<----HERE(Identity National Card(back))
    else:
        pass

    if Carnet == 1:
        contenido.append(Image("./img/Carnet(1).jpg", width=398.88, height=249.96))<----HERE(Card Driver(front))
        contenido.append(Spacer(0,50))
        contenido.append(Image("./img/Carnet(2).jpg", width=398.88, height=249.96))<----HERE(Card Driver(back))
        pass
    
    c.build(contenido)

```
4. Start de App

```
python3 main.py
```