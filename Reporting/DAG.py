import os
from include.extractor_datos import extraer_datos
from include.generador_graficos_MB52 import generar_graficos
from include.envio_correo import enviar_correo
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

ruta_actual = os.path.join(os.path.dirname(
    os.path.dirname(__file__)), "include")
print(ruta_actual)

# Definimos la funcion que ejecuta el primer archivo
def ejecutar_extractor_datos():
    try:
        extraer_datos()
        print("Ejecutando extraccion de datos")
    except Exception as e:
        print(f"Error al extraer los datos: {str(e)}")

# Definimos la funcion que ejecuta el segundo archivo
def ejecutar_generador_graficos():
    try:
        generar_graficos()
        print("Ejecutando generacion de graficos")
    except Exception as e:
        print(f"Error al generar los graficos: {str(e)}")

# Definimos la funcion que ejecuta el tercer archivo
def ejecutar_envio_correo():
    try:
        enviar_correo()
        print("Ejecutando el envio del correo")
    except Exception as e:
        print(f"Error al enviar el reporte: {str(e)}")


# Definimos el dag
dag = DAG(
    'dag_reporting_bayer',
    start_date=datetime(2023, 9, 28),  # Fecha de inicio
    schedule_interval=timedelta(minutes=5),  # Programamos la frecuencia
    catchup=False  # Evitamos la ejecución de tareas anteriores si se configura después
)

# Definimos los operadores
paso_1_task = PythonOperator(
    task_id='extractor_datos',
    python_callable=ejecutar_extractor_datos,
    dag=dag
)

paso_2_task = PythonOperator(
    task_id='generador_graficos',
    python_callable=ejecutar_generador_graficos,
    dag=dag
)

paso_3_task = PythonOperator(
    task_id='envio_correo',
    python_callable=ejecutar_envio_correo,
    dag=dag
)

# Establecemos el orden de ejecución de los operadores
paso_1_task >> paso_2_task >> paso_3_task
