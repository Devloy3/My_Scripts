import pandas as pd
import os
from reportlab.platypus import SimpleDocTemplate,Paragraph,PageBreak
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_CENTER

def enseñar_datos_de_la_caixa(archivo): 
    
    df = pd.read_csv(archivo, sep=';')
    df.columns = df.columns.str.strip()


    gastos = df[df['Importe'] < 0]['Importe'].sum()
    ingresos = df[df['Importe'] > 0]['Importe'].sum()
    ingresos_2 = df[df['Importe'] > 0 ].groupby('Concepto')['Importe'].sum().sort_values(ascending=False)
    gastos_2 = df[df['Importe'] < 0].groupby('Concepto')['Importe'].sum().sort_values(ascending=True)
    
    print(f"\nTotal de Gastos: {gastos:.2f}€")
    print(f"Total de Ingresos; {ingresos:.2f}€")
    print(f"Restante: {ingresos+gastos:.2f}€")

    print("\nIngresos: \n")
    for Concepto, Importe in ingresos_2.items():
        print(f"{Concepto}: {Importe:.2f} --- {Importe/ingresos * 100:.2f}%")
    
    print("\nGastos:\n")
    for Concepto, Importe in gastos_2.items():
        print(f"{Concepto}: {Importe:.2f} --- {-Importe/-gastos * 100:.2f}%")

def hacer_pdf_de_revoult(archivo, periodo):

    ruta = f"../financial/{periodo}"
    os.makedirs(ruta, exist_ok=True)
    
    pdf_path = os.path.join(ruta, "PDF_Sonia.pdf")
    c = SimpleDocTemplate(pdf_path)
    contenido = []
    estilos = getSampleStyleSheet()
    contenido.append(Paragraph("<b>Periodo</b>: 01-01-2025 / 16-09-2025", estilos['Normal']))
    contenido.append(Paragraph("Desglose de Revoult", estilos['Heading1']))

    df = pd.read_csv(archivo)
    df.columns = ['Type        ', ' Product', ' Started Date       ',' Completed Date     ', ' Description                              ',' Amount ', ' Fee ', ' Currency', ' State    ', ' Balance']
    df.columns = df.columns.str.strip()

    estilo_centrado = ParagraphStyle(
        name='Centrado',
        parent= estilos['Normal'],
        alignment=TA_CENTER,
        leading=16
    )

    total_gastos = df[df['Amount'] < 0]['Amount'].sum()
    total_ingresos = df[df['Amount'] > 0]['Amount'].sum()

    gastos = df[df['Amount'] < 0].groupby('Description')['Amount'].sum().sort_values(ascending=True)
    ingresos = df[df['Amount'] > 0].groupby('Description')['Amount'].sum().sort_values(ascending=True)
    
    contenido.append(Paragraph("Gastos", estilos['Heading2']))
    
    for Description, Amount in gastos.items():
        contenido.append(Paragraph(f"<b>{Description}</b>:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{Amount:.2f}€&nbsp;&nbsp;(<b>{Amount/total_gastos*100:.2f}%</b>)", estilo_centrado))
    
    contenido.append(Paragraph(f"<b>Total de gastos</b>: {total_gastos:.2f}€"))

    contenido.append(PageBreak())
    contenido.append(Paragraph("Ingresos", estilos['Heading2']))
    
    for Description, Amount in ingresos.items():
        contenido.append(Paragraph(f"<b>{Description}</b>:&nbsp;{Amount:.2f}€ (<b>{int(Amount / total_ingresos * 100)}</b>%)", estilo_centrado))
    
    contenido.append(Paragraph(f"<b>Total de ingresos</b>: {total_ingresos:.2f}€"))
    contenido.append(Paragraph(f"<b>Restante</b>: {total_ingresos+total_gastos:.2f}€"))
    
    c.build(contenido)


def administracion_de_dinero(salario):

    mitad = float(salario) * 0.50
    parte1 = float(salario) * 0.30 
    parte2 = float(salario) * 0.20

    mini_parte = parte2 * 0.50

    mini_mini_parte = mini_parte * 0.50 

    texto = f'''
            Dinero destinado a casa: {int(mitad)}€
            Dinero para mis gastos propios: {int(parte1)}€
            Dinero para ahorro i inversion:         Total {int(parte2)}€
                    Ahorro:                         Total {int(mini_parte)}€
                        Jubilacion: {int(mini_mini_parte)}€ 
                        Viajes: {int(mini_mini_parte)}€
                    Inversion:                      Total {int(mini_parte)}€
                        Francos Suizos: {int(mini_mini_parte)}€
                        Acciones o Criptomonedas: {int(mini_mini_parte)}€ 
            '''
    
    return texto


def menu():
    while True:
        print("\n <-- Gestion de Finanzas --> \n")
        print("1. Desglosar Gastos y ingresos de la Caixa")
        print("2. PDF, Revoult")
        print("3. Desglosar Salario")
        print("4. Salir")

        option = int(input("Escoge uno:"))

        if option == 1:
            archivo = input("Pon la ruta del Archivo:").strip()
            enseñar_datos_de_la_caixa(archivo)
        elif option == 2:
            archivo = input("Pon la ruta del Archivo:").strip()
            periodo = input("Periodo del Archivo:").strip()
            hacer_pdf_de_revoult(archivo,periodo)
        elif option == 3:
            salario_neto = input("Introduce tu Salario: ")
            texto = administracion_de_dinero(salario_neto)
            print(texto)
        elif option == 4:
            break

menu()

