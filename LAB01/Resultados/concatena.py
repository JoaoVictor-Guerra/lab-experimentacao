import glob
import csv
import pandas as pd

def concatena_csvs(arquivos_csv, arquivo_saida):
    with open(arquivo_saida, 'w', newline='') as arquivo_final:
        writer = None
        for arquivo_csv in arquivos_csv:
            with open(arquivo_csv, 'r', newline='') as csv_file:
                reader = csv.reader(csv_file)
                if writer is None:
                    writer = csv.writer(arquivo_final)
                    writer.writerows(reader)
                else:
                    next(reader)  # Ignora o cabeçalho nos arquivos subsequentes
                    writer.writerows(reader)
    print(f"Arquivos CSV concatenados e salvos em {arquivo_saida}")

nomes_arquivos = ['lab01RQ01.csv', 'lab01RQ02.csv', 'lab01RQ03.csv', 'lab01RQ04.csv', 'lab01RQ05.csv', 'lab01RQ06.csv']

arquivo_saida = 'lab01Results.csv'

concatena_csvs(nomes_arquivos, arquivo_saida)