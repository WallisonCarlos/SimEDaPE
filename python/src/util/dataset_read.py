import pandas as pd
import numpy as np
import glob
import os

def read_csv(data_file, sep = ';', dtype = {"link": int, "length": int, "capacity": int, "freespeed": int}, usecols = ["link", "length", "capacity", "freespeed"]):
    """Função para ler um aquivo csv e retornar um data frame do pandas.

    Parameters:
        data_file (str): Caminho do arquivo para o arquivo CSV do dataset.
        sep (str): Separador do arquivo CSV de entrada.
        dtype (dict): Tipo de dado de cada coluna do arquivo.
        usecols (list): Rótulo de cada coluna.

    Returns:
        DataFrame: Dataframe com as informações do arquivo carregadas.
   """
    data_frame = pd.read_csv(data_file, 
                    sep = sep,
                    engine = 'python',
                    quotechar="'",        
                    dtype=dtype,             
                    usecols=usecols)
    return data_frame

def read_street_info(data_file, sep = ';'):
    """Esse função faz o carregamento das informações de cada rua, id, tamanho, capacidade e velocidade.
    Essas informações são necessárias para calcular algumas métricas, como velocidade média, Km trafegados, etc.

    Parameters:
        data_file (str): Caminho do arquivo para o arquivo com as informações das ruas.
        sep (str): Separador do arquivo CSV de entrada.

    Returns:
        dict: com as informações para cada rua.
   """
    streets_info = {}
    data_frame = read_csv(data_file, sep = sep)
    for (i, row) in data_frame.iterrows():
        info = []
        info.append(row['length'])
        info.append(row['capacity'])
        info.append(row['freespeed'])
        streets_info[str(row['link'])] = info
    return streets_info

def get_time_series_label(name, interval):
    return name[0]+str("-")+str(interval).replace("(", "").replace("]", "").replace(", ", "-")

def read_single_scenario(dir_files, sep = ';', intervals = {"start_time": int, "end_time": int, "interval_size": int}):
    """Função criada para ler o output do cenário pré-processado por um outro script. 
    Onde o arquivo de saída do InterSCSimulator é dividido em vários arquivos. Esses arquivos são 
    divididos de acordo com as ruas que foram trafegadas no decorrer da simulação. O conteúdo dos 
    arquivos são os eventos de entrada e saída das ruas. Para um evento de entrada é somado 1, e de saída subtraído 1.
    Então, se houver dois eventos de entrada e 1 de saída o resultado é: 1, 2, 1 9 (em cada linha).  

    Parameters:
        dir_files (str): Diretório onde encontram-se os aquivos das ruas com os eventos de entrada e saída computados.
        sep (str): Separador dos arquivos CSV de entrada.
        intervals (dict): Dicionário com as informações de tempo de inicio da simulação, tempo de fim e tamanho das séries temporais (tamanho máximo das séries ou intervalos de tempo)

    Returns:
        int: Tamanho da maior série temporal
        list: Lista de séries temporais
        list: Lista de véiculos de cada série temporal, lista posição 0 da série da posição 0
        dict: Dicionário com a lista de véiculos de cada rua
        list: Lista de rótulos de cada série temporal, rótulo posição 0 da série da posição 0
   """

    max_size = -1
    street_series = []
    street_series_vehicles = []
    street_vehicles = {}
    time_series_labels = []
    data_files = glob.glob(dir_files+"*.csv")
    for data_file in data_files:
        data_frame = read_csv(data_file = data_file, sep = sep, dtype= {"time": int, "vehicle": str, "count": int}, usecols = ["count", "vehicle", "time"])
        data_frame['count'].replace('', np.nan, inplace=True)
        data_frame.dropna(subset=['count'], inplace=True)
        name = str(data_file).replace(dir_files, "").split('-')
        groupby_time_interval = data_frame.groupby(pd.cut(data_frame["time"], np.arange(intervals['start_time'], intervals['end_time'] + intervals['interval_size'], intervals['interval_size'])))
        for name_time_interval, group_time_interval in groupby_time_interval:
            s = group_time_interval['count'].tolist()
            v = group_time_interval['vehicle'].tolist()
            if not name[0] in street_vehicles:
                street_vehicles[name[0]] = []
            street_vehicles[name[0]].append(v)
            if len(s) > 1:
                street_series.append(s)
                street_series_vehicles.append(v)
                time_series_labels.append(get_time_series_label(name, name_time_interval))
                if max_size < len(s):
                    max_size = len(s)
    return max_size, street_series, street_series_vehicles, street_vehicles, time_series_labels


def read_percentage_scenarios(dir_paths, sep = ';', intervals = {"start_time": int, "end_time": int, "interval_size": int}):
    data_set_percentage = {}
    data_paths = os.listdir(dir_paths)
    for dir_files in data_paths:
        dir_files_complete = dir_paths+dir_files+'/'
        if os.path.isdir(dir_files_complete):
            print("Read dataset "+dir_files)
            max_size, street_series, street_series_vehicles, street_vehicles, time_series_labels = read_single_scenario(dir_files_complete, sep = sep, intervals = intervals)
            data_set_percentage[dir_files] = {}
            data_set_percentage[dir_files]['max_size'] = max_size
            data_set_percentage[dir_files]['street_series'] = street_series
            data_set_percentage[dir_files]['street_series_vehicles'] = street_series_vehicles
            data_set_percentage[dir_files]['street_vehicles'] = street_vehicles
            data_set_percentage[dir_files]['time_series_labels'] = time_series_labels
    return data_set_percentage, data_paths


        
