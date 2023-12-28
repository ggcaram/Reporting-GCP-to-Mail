import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import ssl
import datetime


def enviar_correo():
    # Datos del remitente: cuaenta de correo de GMAIL y contraseña temporal generada desde el administrador de GMAIL
    remitente = "ejemplo@gmail.com"
    password = "XXXJJJJKLLL"

    # Mail del destinatario
    destinatario = "receptor@gmail.com"

    # Guardamos la fecha de hoy en una variable para agregarlo al asunto
    fecha_actual = datetime.date.today()

    # Guardo la ruta de las imagenes en una variable
    ruta_actual = os.path.join(os.path.dirname(
        os.path.dirname(__file__)), "include")
    ruta_imagenes = os.path.join(os.path.dirname(
        os.path.dirname(__file__)), "include", "Imagenes")
    ruta_xlxs = os.path.join(os.path.dirname(
        os.path.dirname(__file__)), "include", "XLXS", "excel.xlsx")

    # Creamos el mensaje
    mensaje = MIMEMultipart()
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = f"Reporte generico - {fecha_actual}"

    # Asignamos las rutas de las imagenes para respues re correrlas
    ruta_imagen_barras = f"{ruta_imagenes}/barras.webp"
    ruta_imagen_torta = f"{ruta_imagenes}/torta.webp"
    ruta_imagen_histograma = f"{ruta_imagenes}/histograma.webp"
    ruta_imagen_velocimetro = f"{ruta_imagenes}/velocimetro.webp"
    ruta_imagen_graficolinea = f"{ruta_imagenes}/graficolinea.webp"

    # Tomamos la imagen del grafico de barras y le asignamos un id
    with open(ruta_imagen_barras, 'rb') as image_file:
        imagen_barras = MIMEImage(
            image_file.read(), _subtype='svg+xml', name='barras.webp')
        # Agregamos el id para despues adjuntarlo al mensaje
        imagen_barras.add_header('Content-ID', '<id_barras>')
    mensaje.attach(imagen_barras)

    # Tomamos la imagen del grafico de torta y le asignamos un id
    with open(ruta_imagen_torta, 'rb') as image_file:
        imagen_torta = MIMEImage(image_file.read(), name='torta.webp')
        # Agregamos el id para despues adjuntarlo al mensaje
        imagen_torta.add_header('Content-ID', '<id_torta>')
    mensaje.attach(imagen_torta)

    # Tomamos la imagen del grafico 3d y le asignamos un id
    with open(ruta_imagen_histograma, 'rb') as image_file:
        imagen_histograma = MIMEImage(
            image_file.read(), name='histograma.webp')
        # Agregamos el id para despues adjuntarlo al mensaje
        imagen_histograma.add_header('Content-ID', '<id_histograma>')
    mensaje.attach(imagen_histograma)

    # Tomamos la imagen del velocimetro y le asignamos un id
    with open(ruta_imagen_velocimetro, 'rb') as image_file:
        imagen_velocimetro = MIMEImage(
            image_file.read(), name='velocimetro.webp')
        # Agregamos el id para despues adjuntarlo al mensaje
        imagen_velocimetro.add_header('Content-ID', '<id_velocimetro>')
    mensaje.attach(imagen_velocimetro)

    # Tomamos la imagen del grafico de linea y le asignamos un id
    with open(ruta_imagen_graficolinea, 'rb') as image_file:
        imagen_linea = MIMEImage(image_file.read(), name='graficolinea.webp')
        # Agregamos el id para despues adjuntarlo al mensaje
        imagen_linea.add_header('Content-ID', '<id_graficolinea>')
    mensaje.attach(imagen_linea)

    # Tomamos el excel y le asignamos un id
    with open(ruta_xlxs, 'rb') as adjunto_file:
        adjunto_mb52 = MIMEApplication(adjunto_file.read(), name='mb52.xlsx')
        # Agregamos el id para despues adjuntarlo al mensaje
        adjunto_mb52.add_header('Content-ID', '<id_mb52>')
    mensaje.attach(adjunto_mb52)

    # Armamos el contenido del mail
    conentenidoHtml = f"""\
    <html>
    <head>
    <meta charset="UTF-8">
    <title>Reporte Diario</title>
    </head>
    <body>
    <h2>Buenos días estimados,</h2>
    <h2>Les compartimos el reporte diario inventario</h2>
    <p>Via adjunto ademas agregamos el archivo en excel y los graficos interactivos</p>
    <h5>Cantidad de cada material</h5>
    <img src="cid:id_histograma" alt="Histograma">
    <h5>Materiales en cada lote</h5>
    <img src="cid:id_torta" alt="Torta">
    <h5>Alerta por cantidades bloqueadas</h5>
    <img src="cid:id_velocimetro" alt="Velocimetro">
    <h5>Inventario sin restringir por planta</h5>
    <img src="cid:id_barras" alt="Barras">
    <h5>Stock historico por tipo</h5>
    <img src="cid:id_graficolinea" alt="Linea">
    <h3>Pueden remitirse a la fuente de datos desde el siguiente link: <a href="https://www.sharepoint.com">Sharepoint</a>.</h3>
    <p>Cualquier duda estamos a disposicion.
    Un saludo. </p>
    </body>
    </html>
    """
    # Agregamos al mensaje el contenido del bloque html
    mensaje.attach(MIMEText(conentenidoHtml, 'html'))

    # Servidor SMTP
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587  # gmail port
    SENDER_EMAIL = 'ejemplo@gmail.com'
    SENDER_PW = 'XXXJJJJKLLL'
    WARNING_PEOPLE_EMAILS = ['receptor@gmail.com']

    # Conectamos y enviamos el correo
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)  # security
            server.login(SENDER_EMAIL, SENDER_PW)
            server.sendmail(SENDER_EMAIL, WARNING_PEOPLE_EMAILS,
                            mensaje.as_string())
        # logging.info('EMAIL SENT SECCESSFULLY')
    except Exception as e:
        print("Error al enviar el correo:", str(e))
