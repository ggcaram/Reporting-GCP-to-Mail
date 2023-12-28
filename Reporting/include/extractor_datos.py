import os
import pandas_gbq
from google.oauth2 import service_account


def extraer_datos():
    # Definimos el id de proyecto y ruta de la llave
    PROJECT_ID = 'id-curso-kubernetes'

    ruta_actual = os.path.join(os.path.dirname(
        os.path.dirname(__file__)), "include")
    ruta_key = os.path.join(os.path.dirname(
        os.path.dirname(__file__)), "include", "KEY")
    ruta_csv = os.path.join(os.path.dirname(os.path.dirname(
        __file__)), "include", "CSV", "procesado.csv")

    CREDENTIALS_JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(
        __file__)), "include", "KEY", "id-curso-kubernetes-1111c111111.json")

    # Tomamos las credenciales del json
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_JSON_PATH
    )

    # Seteamos credenciales e id
    pandas_gbq.context.credentials = credentials
    pandas_gbq.context.project = PROJECT_ID

    # Armamos la query
    query = """
        SELECT * 
        FROM `id-curso-kubernetes` 
        LIMIT 40
    """

    # Guardamos el contenido de la query en un dataframe
    data_frame = pandas_gbq.read_gbq(query)

    # Guardamos el contenido del dataframe como csv
    # ruta_archivo = 'CSV/procesado.csv'
    data_frame.to_csv(ruta_csv, index=False)
