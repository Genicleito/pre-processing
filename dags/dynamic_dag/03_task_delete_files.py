import os, sys, inspect
import datetime

print('Datetime:', datetime.datetime.now())
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

print('Removendo arquivos...')
if os.system(f'rm -r {currentdir}/cases-brazil-cities-time.csv') != 0: raise ValueError(f'Erro ao remover arquivo {currentdir}/cases-brazil-cities-time.csv')
print(f'Arquivo {currentdir}/cases-brazil-cities-time.csv removido!')
