# Databricks notebook source
dbutils.widgets.text("data_execucao", "")
data_execucao = dbutils.widgets.get("data_execucao")


# COMMAND ----------

import requests
from pyspark.sql.functions import lit

# COMMAND ----------

def extraindo_dados(date, base="BRL"):

    url = f"https://api.apilayer.com/exchangerates_data/{date}&base={base}"

    headers = {
    "apikey": "xt3X5LJva37vO61zQYyP57o52PifEIPP"
    }

    parametros = {"base":base}
    
    response = requests.request("GET", url, headers=headers, params= parametros)

    if response.status_code != 200:
        raise Exception("Não consegui extrair dados!!!")

    return response.json()


# COMMAND ----------

def dados_dataframe(dados_json):
    tupla = [(moeda, float(taxa))for moeda, taxa in dados_json['rates'].items()]
    return tupla

# COMMAND ----------

def salvando_arquivo(extraindo_dados):
    ano, mes, dia = extraindo_dados['date'].split('-')
    caminho = f"/results/bronze/{ano}/{mes}/{dia}"
    response = dados_dataframe(extraindo_dados)
    df = spark.createDataFrame(response, schema=['moeda', 'taxa'])
    df = df.withColumn('data', lit(f"{ano}-{mes}-{dia}"))
    df.write.format('parquet')\
            .mode("overwrite")\
                .save(caminho)
    
    print(f'Sucesso! Dados salvos em: {caminho}')


# COMMAND ----------

dados_json = extraindo_dados(data_execucao)
salvando_arquivo(dados_json)
