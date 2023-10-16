# Databricks notebook source
from pyspark.sql.functions import to_date, first, col, round

# COMMAND ----------

df_junto = spark.read.parquet("/results/bronze/*/*/*")

# COMMAND ----------

moedas = ['USD', 'EUR', 'GBP']

df_moedas = df_junto.filter(df_junto.moeda.isin(moedas))

# COMMAND ----------

df_moedas = df_moedas.withColumn("data", to_date("data"))

# COMMAND ----------

resultado_taxas_conversao = df_moedas.groupBy("data") \
           .pivot("moeda") \
           .agg(first("taxa")) \
           .orderBy("data", ascending=False)

resultado_valores_reais = resultado_taxas_conversao.select("*")

# COMMAND ----------

for moeda in moedas: 
        resultado_valores_reais = resultado_valores_reais\
                                .withColumn(
                                            moeda, round(1/col(moeda), 4)
                                            )


# COMMAND ----------

resultado_taxas_conversao = resultado_taxas_conversao.coalesce(1)
resultado_valores_reais = resultado_valores_reais.coalesce(1)

# COMMAND ----------

resultado_taxas_conversao.write\
    .mode ("overwrite")\
    .format("csv")\
    .option("header", "true")\
    .save("dbfs:/results/prata/taxas_conversao")
    
resultado_valores_reais.write\
    .mode ("overwrite")\
    .format("csv")\
    .option("header", "true")\
    .save("dbfs:/results/prata/valores_reais")


# COMMAND ----------

print("Sucesso!!")
