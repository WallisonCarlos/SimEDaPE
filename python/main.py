import numpy as np
from jproperties import Properties
from datetime import datetime
import sys
import os

sys.path.append('src/util')
sys.path.append('src/clustering')
sys.path.append('src/scaler')

from src.util.dataset_read import read_single_scenario, read_street_info, read_percentage_scenarios
from src.util.save_data import load_file_to_json, save_clustering, save_file_json
from src.clustering.clustering import proccess_dataset, clustering, silumlation_points_vehicles, simulation_points_indexs, time_series_labels_indexs, simulation_points_labels, warping_path_calculation
from src.util.estimation import estimate, estimation, pre_processing_estimation

configs = Properties()

configs_file = sys.argv[2] if (len(sys.argv) > 0 & (not sys.argv[2] == None) & (not sys.argv[2] == '')) else 'default'

with open('properties/'+configs_file+'.properties', 'rb') as config_file:
    configs.load(config_file)

print('Config file '+str(configs_file)+' loaded')

now = datetime.now()
timestamp = datetime.timestamp(now)
output_folder =  'output/'+str(configs.get('scenario.name').data)

if sys.argv[1] == 'clustering':
    print("Start process...")
    time_series_size, street_series, street_series_vehicles, street_vehicles, time_series_labels  = read_single_scenario(configs.get('scenario.single.dir.files').data, sep = configs.get('csv.sep').data, intervals = {'start_time': int(configs.get('intervals.start_time').data), 'end_time': int(configs.get('intervals.end_time').data), 'interval_size': int(configs.get('intervals.interval_size').data)})
    number_of_time_series = len(street_series)
    print('Time Series Size: '+str(time_series_size))
    print('Number of time series: '+str(number_of_time_series))
    X, mean, std = proccess_dataset(street_series, time_series_size)
    ks, y_pred = clustering(X, n_clusters = int(configs.get('clustering.n_clusters').data), verbose = configs.get('clustering.verbose').data == 'True', random_state = int(configs.get('clustering.random_state').data), max_iter = int(configs.get('clustering.max_iter').data))
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    print("Saving results...")
    save_clustering(file = output_folder+'/'+str(configs.get('clustering.output.save.file').data), ks = ks, y_pred = y_pred, std = std, mean = mean)
    save_file_json(output_folder+'/'+'street_series_vehicles', street_series_vehicles)
    clustering = load_file_to_json(output_folder+'/'+str(configs.get('clustering.output.save.file').data))
    ts_labels_indexs = time_series_labels_indexs(time_series_labels)
    save_file_json(output_folder+'/'+'time_series_labels_indexs', ts_labels_indexs)
    sp_indexs = simulation_points_indexs(clustering, ts_labels_indexs, X)
    save_file_json(output_folder+'/'+'simulation_points_indexs', [int(x) for x in sp_indexs])
    sp_labels = simulation_points_labels(time_series_labels, sp_indexs)
    save_file_json(output_folder+'/'+'simulation_points_labels', sp_labels)
    sp_vehicles = silumlation_points_vehicles(street_vehicles, sp_labels)
    save_file_json(output_folder+'/'+'simulation_points_vehicles', sp_labels)
    print("Process finished!")
elif sys.argv[1] == 'warping_path':
    print('Start warping path calculation...')
    streets_info = read_street_info(configs.get('scenario.single.dir.street.info').data, sep = configs.get('csv.sep').data)
    time_series_size, street_series, street_series_vehicles, street_vehicles, time_series_labels  = read_single_scenario(configs.get('scenario.single.dir.files').data, sep = configs.get('csv.sep').data, intervals = {'start_time': int(configs.get('intervals.start_time').data), 'end_time': int(configs.get('intervals.end_time').data), 'interval_size': int(configs.get('intervals.interval_size').data)})
    number_of_time_series = len(street_series)
    print('Time Series Size: '+str(time_series_size))
    print('Number of time series: '+str(number_of_time_series))
    X, mean, std = proccess_dataset(street_series, time_series_size)
    clustering = load_file_to_json(output_folder+'/'+str(configs.get('clustering.output.save.file').data))
    ts_labels_indexs = time_series_labels_indexs(time_series_labels)
    wps = warping_path_calculation(clustering, ts_labels_indexs, X)
    save_file_json(output_folder+'/'+'warping_path', wps)
    print('End warping path calculation...')
elif sys.argv[1] == 'metrics': 
    streets_info = read_street_info(configs.get('scenario.single.dir.street.info').data, sep = configs.get('csv.sep').data)
elif sys.argv[1] == 'single_estimation':
    streets_info = read_street_info(configs.get('scenario.single.dir.street.info').data, sep = configs.get('csv.sep').data)
    print("Start process...")
    time_series_size, street_series, street_series_vehicles, street_vehicles, time_series_labels  = read_single_scenario(configs.get('scenario.single.dir.files').data, sep = configs.get('csv.sep').data, intervals = {'start_time': int(configs.get('intervals.start_time').data), 'end_time': int(configs.get('intervals.end_time').data), 'interval_size': int(configs.get('intervals.interval_size').data)})
    number_of_time_series = len(street_series)
    print('Time Series Size: '+str(time_series_size))
    print('Number of time series: '+str(number_of_time_series))
    X, mean, std = proccess_dataset(street_series, time_series_size)
    
    clustering = load_file_to_json(output_folder+'/'+str(configs.get('clustering.output.save.file').data))
    wps = load_file_to_json(output_folder+'/warping_path')
    
    time_series_size_2, street_series_2, street_series_vehicles_2, street_vehicles_2, time_series_labels_2  = read_single_scenario(configs.get('estimation.second.scenario.dir.files').data, sep = configs.get('csv.sep').data, intervals = {'start_time': int(configs.get('intervals.start_time').data), 'end_time': int(configs.get('intervals.end_time').data), 'interval_size': int(configs.get('intervals.interval_size').data)})
    number_of_time_series_2 = len(street_series)
    print('Time Series Size Second: '+str(time_series_size_2))
    print('Number of time series Second: '+str(number_of_time_series_2))
    X_2, mean_2, std_2 = proccess_dataset(street_series_2, time_series_size_2)

    print(len(X_2))

    time_series_labels_indexs_first, time_series_labels_dict_first = pre_processing_estimation(time_series_labels)
    time_series_labels_indexs_second, time_series_labels_dict_second = pre_processing_estimation(time_series_labels_2)

    simulation_points_indexs = load_file_to_json(output_folder+'/simulation_points_indexs')

    metrics = estimation(streets_info, clustering, wps, mean, std, mean_2, std_2, X_2, time_series_labels_indexs_first, time_series_labels, time_series_labels_dict_first, time_series_labels_dict_second, simulation_points_indexs, printer = True)
    print("End process...")
elif sys.argv[1] == 'multiple_estimation':
    streets_info = read_street_info(configs.get('scenario.single.dir.street.info').data, sep = configs.get('csv.sep').data)
    print("Start process...")

    time_series_size, street_series, street_series_vehicles, street_vehicles, time_series_labels  = read_single_scenario(configs.get('scenario.single.dir.files').data, sep = configs.get('csv.sep').data, intervals = {'start_time': int(configs.get('intervals.start_time').data), 'end_time': int(configs.get('intervals.end_time').data), 'interval_size': int(configs.get('intervals.interval_size').data)})
    number_of_time_series = len(street_series)
    print('Time Series Size: '+str(time_series_size))
    print('Number of time series: '+str(number_of_time_series))
    X, mean, std = proccess_dataset(street_series, time_series_size)
    
    clustering = load_file_to_json(output_folder+'/'+str(configs.get('clustering.output.save.file').data))
    wps = load_file_to_json(output_folder+'/warping_path')
    
    data_set_percentage, data_paths = read_percentage_scenarios(configs.get('estimation.second.percentage.scenarios.dir.files').data, configs.get('csv.sep').data, {'start_time': int(configs.get('intervals.start_time').data), 'end_time': int(configs.get('intervals.end_time').data), 'interval_size': int(configs.get('intervals.interval_size').data)})
    
    for dir_files in data_paths:
        print("Scenario "+str(dir_files))
        time_series_size_2 = data_set_percentage[dir_files]['max_size']
        street_series_2 = data_set_percentage[dir_files]['street_series']
        street_series_vehicles_2 = data_set_percentage[dir_files]['street_series_vehicles']
        street_vehicles_2 = data_set_percentage[dir_files]['street_vehicles']
        time_series_labels_2 = data_set_percentage[dir_files]['time_series_labels']
        number_of_time_series_2 = len(street_series)
        print('Time Series Size Second: '+str(time_series_size_2))
        print('Number of time series Second: '+str(number_of_time_series_2))
        X_2, mean_2, std_2 = proccess_dataset(street_series_2, time_series_size)

        print(len(X_2))

        time_series_labels_indexs_first, time_series_labels_dict_first = pre_processing_estimation(time_series_labels)
        time_series_labels_indexs_second, time_series_labels_dict_second = pre_processing_estimation(time_series_labels_2)

        simulation_points_indexs = load_file_to_json(output_folder+'/simulation_points_indexs')

        metrics = estimation(streets_info, clustering, wps, mean, std, mean_2, std_2, X_2, time_series_labels_indexs_first, time_series_labels, time_series_labels_dict_first, time_series_labels_dict_second, simulation_points_indexs, printer = True, multiple = True)
        
    print("End process...")