# Databricks notebook source
# MAGIC %pip install kaleido slack-sdk

# COMMAND ----------

from slack_sdk import WebClient
import pyspark.pandas as ps

# COMMAND ----------

slack_token = "xoxb-6041421187155-6041546447938-SR1AcDUDmk2trzeovAU2ii1O"
client = WebClient(token=slack_token)

# COMMAND ----------

nome_arquivo = dbutils.fs.ls("dbfs:/results/prata/valores_reais/")[-1].name

# COMMAND ----------

path =  "../../../../dbfs/results/prata/valores_reais/" + nome_arquivo

# COMMAND ----------

enviando_arquivo_csv = client.files_upload_v2(
    channel="C061WF1GSHE",  
    title="Arquivo no formato CSV do valor do real convertido",
    file=path,
    filename="valores_reais.csv",
    initial_comment="Segue anexo o arquivo CSV:",
)


# COMMAND ----------

df_valores_reais = ps.read_csv("dbfs:/results/prata/valores_reais/")

# COMMAND ----------

for moeda in df_valores_reais.columns[1:]:
    fig = df_valores_reais.plot.line(x="data", y=moeda)
    fig.write_image(f"../../../../dbfs/results/imagem/{moeda}.png")

# COMMAND ----------

def enviando_imagens(moeda):
    enviando_arquivo_csv = client.files_upload_v2(
    channel="C061WF1GSHE",  
    title="Enviado imagens de cotações",
    file=f"../../../../dbfs/results/imagem/{moeda}.png",
)


# COMMAND ----------

for moeda in df_valores_reais.columns[1:]:
    enviando_imagens(moeda)

# COMMAND ----------


