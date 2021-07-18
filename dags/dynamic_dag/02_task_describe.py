import pyspark.sql.functions as F
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession

from IPython import display
import pandas as pd
import os, sys, inspect
import datetime
from tqdm import tqdm

sc = SparkContext()
spark = SparkSession(sc)

pd.set_option("max_rows", None)
pd.set_option("max_columns", None)
pd.set_option("max_colwidth", None)

print('Datetime:', datetime.datetime.now())
print('AppID:', sc.applicationId)

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
df = spark.read.csv(f'{currentdir}/cases-brazil-cities-time.csv', header=True, inferSchema=True, multiLine=True)

ts = datetime.datetime.now()
print('Realizando describe dos dados...')
df.summary().show(20, False) # .toPandas().set_index('summary').T)
print('Tempo do describe:', datetime.datetime.now() - ts)

def describe(df, columns=None):
    if not columns: columns = df.columns
    if not isinstance(columns, list): columns = [columns]
    return pd.DataFrame({
        col: {
                'count': df.count(), 
                f'notNull': df.filter(F.col(col).isNotNull()).count(),
                f'uniqueNotNull': df.filter(F.col(col).isNotNull()).select(col).distinct().count(),
                f'duplicatesNotNull': df.filter(F.col(col).isNotNull()).count() - df.filter(F.col(col).isNotNull()).select(col).distinct().count(),
            } for col in columns
        })

for i, col in enumerate(df.columns):
    print(f'{i + 1} / {len(df.columns)}')
    df.groupBy(col).count().orderBy(F.col('count').desc()).show(30, False)

df_info = describe(df)
display.display(df_info)

print('Tempo de execução:', datetime.datetime.now() - ts)
