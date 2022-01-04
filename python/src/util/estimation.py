import math
import numpy as np
import time
from metrics import average_vehicles_track, calcPercentaceOfTrack, getAvegareSpeedOfTrack, kilometers_traveled
from scipy.stats import gmean

def get_serie_from(data, time_series_labels_dict, time_series_labels, time_series_index):
    return data[time_series_labels_dict[time_series_labels[time_series_index]]].ravel().astype(float)

def get_serie_index_from(time_series_labels_dict, time_series_labels, time_series_index):
    return time_series_labels_dict[time_series_labels[time_series_index]]

def check_serie_scenario2_from(time_series_labels_dict, time_series_labels, time_series_index):
    return time_series_labels[time_series_index] in time_series_labels_dict

def increment(number):
    return number + 1

def time_translation(path, s):
    serie = np.zeros(len(s))
    t = path[0]
    if t[3] == True:
        serie[t[1]] = s[t[0]] - t[2]
    else:
        serie[t[1]] = s[t[0]] + t[2]
    for pos in range(1, len(path)):
        t = path[pos]
        before = path[pos - 1]
        if t[3] == True:
            serie[t[1]] = s[t[0]] - math.sqrt(t[2]**2 - before[2]**2)
        else:
            serie[t[1]] = math.sqrt(t[2]**2 - before[2]**2) + s[t[0]] 
    return serie

def estimate(time_series, warping_path, std, mean):
    series_translation = time_translation(warping_path[0], time_series)
    series_translation_revert = series_translation * std + mean
    return series_translation_revert

def get_link_id_from(time_series_labels):
  link_id = time_series_labels.split("-")
  return link_id[0]

def scale_revert(time_series, std, mean):
    return time_series * std + mean

def time_series_estimate_error(estimate, original):
    return np.sum(np.abs(original - estimate))

def percentage_error_metric(real, estimate):
    return 100 * ((estimate - real) / real)

def calc_metrics(serie, link_id, links_info, serie_name = "Serie name", printer = False):
    calc = {}
    average_speed = getAvegareSpeedOfTrack(serie, link_id, links_info)
    calc['average_speed'] = average_speed
    percentage_of_track = calcPercentaceOfTrack(serie, link_id, links_info)
    calc['percentage_of_track'] = percentage_of_track
    average_vehicles = average_vehicles_track(serie)
    calc['average_vehicles'] = average_vehicles
    link_info = links_info[link_id]
    km_traveled = kilometers_traveled(link_info[0], serie)
    calc['km_traveled'] = km_traveled
    if printer:
        print("\t\t"+serie_name)
        print("\t\t\tAverage Speed: "+str(average_speed)+"m/s")
        print("\t\t\tPercentage vehicles of track: "+str(percentage_of_track)+"%")
        print("\t\t\tAverage Vehicles: "+str(average_vehicles))
        print("\t\t\tKm Traveled: "+str(km_traveled)+"Km")
    return calc

def calc_estimate_errors(calc1, calc2, printer = False):
    error = {}
    error['average_speed'] = percentage_error_metric(calc1['average_speed'], calc2['average_speed'])
    error['percentage_of_track'] = percentage_error_metric(calc1['percentage_of_track'], calc2['percentage_of_track'])
    error['average_vehicles'] = percentage_error_metric(calc1['average_vehicles'], calc2['average_vehicles'])
    error['km_traveled'] = percentage_error_metric(calc1['km_traveled'], calc2['km_traveled'])
    if printer:
        print("\t\t\tErro:")
        print("\t\t\t\tAverage Speed: "+str(error['average_speed'])+"%")
        print("\t\t\t\tPercentage vehicles of track: "+str(error['percentage_of_track'])+"%")
        print("\t\t\t\tAverage Vehicles: "+str(error['average_vehicles'])+"%")
        print("\t\t\t\tKm Traveled: "+str(error['km_traveled'])+"%")
    return error

def append_errors(errors_list, error):
    errors_list['average_speed'].append(error['average_speed'])
    errors_list['percentage_of_track'].append(error['percentage_of_track'])
    errors_list['average_vehicles'].append(error['average_vehicles'])
    errors_list['km_traveled'].append(error['km_traveled'])
    return errors_list

def def_errors_list():
    errors_list = {}
    errors_list['average_speed'] = []
    errors_list['percentage_of_track'] = []
    errors_list['average_vehicles'] = []
    errors_list['km_traveled'] = []
    return errors_list

def def_errors_list_g():
    errors_list = {}
    errors_list['average_speed'] = []
    errors_list['percentage_of_track'] = []
    errors_list['average_vehicles'] = []
    errors_list['km_traveled'] = []
    return errors_list

def def_bigger_errors():
    bigger_errors = {}
    bigger_errors['average_speed'] = -1
    bigger_errors['percentage_of_track'] = -1
    bigger_errors['average_vehicles'] = -1
    bigger_errors['km_traveled'] = -1
    return bigger_errors

def def_bigger_errors_g():
    bigger_errors = {}
    bigger_errors['average_speed'] = -1
    bigger_errors['percentage_of_track'] = -1
    bigger_errors['average_vehicles'] = -1
    bigger_errors['km_traveled'] = -1
    return bigger_errors

def estimation(links_info, clustering, wps, mean, std, mean_2, std_2, X_2, time_series_labels_first_indexs, time_series_labels_first, time_series_labels_first_dict, time_series_labels_second_dict, simulation_points_indexs, printer = False):
    start_time = time.time()
    print(start_time)
    metrics = {}
    metrics['average_speed'] = []
    metrics['percentage_of_track'] = []
    metrics['average_vehicles'] = []
    metrics['km_traveled'] = []
    time_series_labels_first_indexs = np.array(time_series_labels_first_indexs)
    for i in range(clustering['number_of_clusters']):
        print("====================== Simulation Point "+str(i)+" ==============================")
        for k in time_series_labels_first_indexs[np.array(clustering['clusters']) == i]:
            if (check_serie_scenario2_from(time_series_labels_second_dict, time_series_labels_first, simulation_points_indexs[i])):
                warping_path = wps['warping_paths'][str(i)][str(k)]
                
                std_s2 = std[get_serie_index_from(time_series_labels_first_dict, time_series_labels_first, k)][0][0]
                mean_s2 = mean[get_serie_index_from(time_series_labels_first_dict, time_series_labels_first, k)][0][0]
                std_s23 = std_2[get_serie_index_from(time_series_labels_second_dict, time_series_labels_first, k)][0][0]
                mean_s23 = mean_2[get_serie_index_from(time_series_labels_second_dict, time_series_labels_first, k)][0][0]
                std_s2 = (std_s2 + std_s23) / 2
                mean_s2 = (mean_s2 + mean_s23) / 2
                w1 = get_serie_from(X_2, time_series_labels_second_dict, time_series_labels_first, simulation_points_indexs[i])
                serie_translation_revert = estimate(w1, warping_path, std_s2, mean_s2)
                link_id = get_link_id_from(time_series_labels_first[k])
                
                calc = calc_metrics(serie_translation_revert, link_id, links_info, "Second complete - "+str(link_id), printer)
                metrics['average_speed'].append(calc['average_speed'])
                metrics['percentage_of_track'].append(calc['percentage_of_track'])
                metrics['average_vehicles'].append(calc['average_vehicles'])
                metrics['km_traveled'].append(calc['km_traveled'])
            else:
                print("Simulation Point não gerado no segundo cenário!!!")

    print("Average Speed: ", gmean(metrics['average_speed']))
    print("Percentage of track: ", gmean(metrics['percentage_of_track']))
    print("Average Vehicles: ", gmean(metrics['average_vehicles']))
    print("Km Traveled: ", gmean(metrics['km_traveled']))
    end_time = time.time()
    print(end_time)
    print("Time: ", end_time - start_time)
    return metrics

def pre_processing_estimation(time_series_labels):
    time_series_labels_indexs = []
    for i in range(len(time_series_labels)):
        time_series_labels_indexs.append(i)
    time_series_labels_dict = {}
    for i in range(len(time_series_labels)):
        time_series_labels_dict[time_series_labels[i]] = i
    return time_series_labels_indexs, time_series_labels_dict