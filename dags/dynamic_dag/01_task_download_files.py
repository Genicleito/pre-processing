import pandas as pd
import datetime
import os, sys, inspect
import datetime
from tqdm import tqdm
from IPython import display
print('Datetime:', datetime.datetime.now())

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
read_path = 'https://github.com/wcota/covid19br/raw/master/cases-brazil-cities-time.csv.gz'
write_path = f'{currentdir}/cases-brazil-cities-time.csv'

ts = datetime.datetime.now()
print('Baixando dados...')
df = pd.read_csv(read_path).reset_index()
print('Baixados dados de:', df['date'].max())

df.to_csv(write_path, index=False)
print('Tempo para baixar e escrever os dados:', datetime.datetime.now() - ts)
df.info()

print('Tempo de execução:', datetime.datetime.now() - ts)
