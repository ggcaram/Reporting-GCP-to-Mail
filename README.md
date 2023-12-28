# Reporting-GCP-to-Mail
Reporting project that extracts data from GCP, graphs it and sends it by email orchestrated with airflow
<img width="712" alt="diagrama" src="https://github.com/ggcaram/Reporting-GCP-to-Mail/assets/63132435/810a545d-bc2e-4f2f-9728-d29e79f9723e">


The proyect is divided in 4 steps
1) extractor_datos.py: Using a query with BigQuery we extract the data from a database, convert it to dataframe with pandas and save it in .csv format.
The purpose of performing this as a separate step is to orchestrate it in Airflow so that it is repeated only once per day and saved, avoiding repeating the query.
<img width="485" alt="image" src="https://github.com/ggcaram/Reporting-GCP-to-Mail/assets/63132435/2724610a-0134-45e8-aedd-c257c73d38eb">

2) generador_graficos.py:
-Assignment of saving paths for images, excel files and the html of the final report. 
-I assemble all graphs and attachments, using Plotly Express and Graph Objects.
-We save the generated in local paths (can be changed to a drive or sharepoint).
3) envio_correo.py:
<img width="169" alt="image" src="https://github.com/ggcaram/Reporting-GCP-to-Mail/assets/63132435/c08d63ba-d557-4836-9b18-fc801863d0ec">

4) envio_correo.py:
Taking all the files saved before, we assemble the HTML report and send the mail with the complete report.
4) DAG.py:
<img width="164" alt="image" src="https://github.com/ggcaram/Reporting-GCP-to-Mail/assets/63132435/0afc6175-8aaf-44f3-b25e-b6853bd572e6">

6) DAG.py:
We nest the tasks and run the chain in Airflo to send the complete report.
