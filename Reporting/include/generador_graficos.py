import os
import pandas as pd
import plotly.express as px
from plotly import graph_objects as go


def generar_graficos():
    # Guardo las rutas que voy a usar en variables 
    ruta_actual = os.path.join(os.path.dirname(os.path.dirname(__file__)),"include")
    ruta_html = os.path.join(os.path.dirname(os.path.dirname(__file__)),"include", "Html")
    ruta_imagenes = os.path.join(os.path.dirname(os.path.dirname(__file__)),"include", "Imagenes")
    ruta_xlxs = os.path.join(os.path.dirname(os.path.dirname(__file__)),"include", "XLXS")

    # Tomamos los datos de la fuente 
    data_frame = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)),"include", "CSV", "procesado.csv"))

    # Guardamos como excel
    ruta_archivo_excel = os.path.join(os.path.dirname(os.path.dirname(__file__)),"include", "XLXS", "excel.xlsx")
    data_frame.to_excel(ruta_archivo_excel, index=False)

    # Agrupamos los materiales por lote
    materiales_lote = data_frame.groupby('Material')['Batch'].count().reset_index()

    # Armamos el grafico de torta
    traza_torta = go.Pie(labels=data_frame.Batch, values=materiales_lote.Batch, title='Materiales por lote')

    # Armamos el grafico de barra 
    traza_barras = px.bar(data_frame, x="Unrestricted", y="Plant", color="Material_Description",barmode="group",title='Unrestricted Qty x Plant')

    # Armamos los agrupamientos por tipo de stock y guardamos en distintos dataframes
    suma_bloqueado= data_frame.groupby('Date_of_Manufacture')['Blocked'].sum().reset_index()
    suma_unrestricted= data_frame.groupby('Date_of_Manufacture')['Unrestricted'].sum().reset_index()
    suma_in_quality= data_frame.groupby('Date_of_Manufacture')['In_Quality_Insp_'].sum().reset_index()
    suma_stock_in_transfer= data_frame.groupby('Date_of_Manufacture')['Stock_in_transfer'].sum().reset_index()

    # Combinamos los dataframe's
    combined_df = pd.concat([suma_bloqueado, suma_unrestricted, suma_in_quality,suma_stock_in_transfer], ignore_index=True)

    # Armamos el grafico de linea
    traza_linea= px.line(combined_df, x= "Date_of_Manufacture", y=["Blocked", "Unrestricted","In_Quality_Insp_","Stock_in_transfer"])

    # Modificamos el layout
    traza_linea.update_traces(patch={"line":{"dash":"dot","shape":"spline"}})
    traza_linea.update_layout(title="Inventario anual",
        legend={"title":"Tipo de stock"},
        xaxis_title="Año",
        yaxis_title="Cantidad")

    # Armamos el histograma
    traza_histograma= px.histogram(data_frame, x="Material_Description",nbins=2, color="Material_Description")
    # Modificamos el layout
    traza_histograma.update_layout(title="Cantidad x Material",
        xaxis_title="Material",
        yaxis_title="Cantidad")

    # Armamos el grafico de velocimetro
    # Definimos el campo que queremos mostrar en el velocimetro
    cantidad_bloqueada = data_frame['Blocked'].sum()

    # Creamos el velocimetro
    traza_velocimetro = go.Figure()
    traza_velocimetro.add_trace(go.Indicator(
        mode="gauge+number",
        value=cantidad_bloqueada,
        title={'text': "Cantidad bloqueada"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, 1000]},
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 300
            }
        }
    ))

    # Editamos el layout del velocimetro
    traza_velocimetro.update_layout(
        title="Velocímetro",
        font=dict(size=16),
        polar_bgcolor='lightgray',
        polar_radialaxis_showticklabels=False,
        polar_angularaxis_showticklabels=False,
        polar_angularaxis_showline=False,
        polar_radialaxis_showline=False,
        showlegend=False
    )

    # Función para guardar un gráfico en formato HTML
    def guardar_graficos_html(figura, nombre_archivo):
        traza = go.Figure(figura)
        rutas_html = os.path.join(ruta_html, nombre_archivo)
        traza.write_html(rutas_html)

    # Guardar los gráficos usando la función
    guardar_graficos_html(traza_barras, "barras.html")
    guardar_graficos_html(traza_torta, "torta.html")
    guardar_graficos_html(traza_linea, "graficolinea.html")
    guardar_graficos_html(traza_histograma, "histograma.html")
    guardar_graficos_html(traza_velocimetro, "velocimetro.html")

    def guardar_graficos_webp(figura_imagenes, nombre_archivo_imagen):
        traza_imagenes = go.Figure(figura_imagenes)
        rutas_imagenes = os.path.join(ruta_imagenes, nombre_archivo_imagen)
        traza_imagenes.write_image(rutas_imagenes)
        print("Esta funcionando o no...")

    # Guardar los gráficos usando la función
    guardar_graficos_webp(traza_barras, "barras.webp")
    guardar_graficos_webp(traza_torta, "torta.webp")
    guardar_graficos_webp(traza_linea, "graficolinea.webp")
    guardar_graficos_webp(traza_histograma, "histograma.webp")
    guardar_graficos_webp(traza_velocimetro, "velocimetro.webp")


    # Lista los nombres de todos los graficos guardados como html
    nombres_graficos = ["barras.html", "torta.html", "graficolinea.html", "histograma.html", "velocimetro.html"]

    # Tamos todos los graficos de la lista para asignar la ruta correspondiente
    archivos_html = [f"{ruta_html}/{nombre}" for nombre in nombres_graficos]

    # Inicializamos una cadena de texto para almacenar el contenido combinado
    contenido_combinado = ""

    # Tomamos cada archivo, lo leemos y gregamos el contenido a la cadena
    for archivo in archivos_html:
        with open(archivo, "r", encoding="utf-8") as file:
            contenido_archivo = file.read()
            contenido_combinado += contenido_archivo

    # Nombramos y asignamos la ruta del archivo combinado
    archivo_html_combinado = os.path.join(os.path.dirname(os.path.dirname(__file__)),"include","HTML", "Reporte_completo.html")

    # Agregamos el contenido combinado a la
    with open(archivo_html_combinado, "w", encoding="utf-8") as file:
        file.write(contenido_combinado)
