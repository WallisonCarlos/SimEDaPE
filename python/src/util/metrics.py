import numpy as np
from scipy.stats import gmean

def get_average_speed(street_length, street_freespeed, time_serie, alpha = 1.0, beta = 1.0, cell_size = 7.5):
    capacity = street_length / cell_size
    #Freespeed * math:pow(1 - math:pow((NumberCars / Capacity), Beta), Alpha) - retirado da tese e do simulador
    time_serie_average_speed = []
    for i in range(len(time_serie)):
        if time_serie[i] >= capacity:
            time_serie_average_speed.append(1)
        else:
            time_serie_average_speed.append(street_freespeed * np.power(1 - np.power((time_serie[i] / capacity), beta), alpha))
    return time_serie_average_speed

def percentage_of_track(street_length, time_serie, cell_size = 7.5):
    capacity = street_length / cell_size
    return (time_serie / capacity) * 100

def kilometers_traveled(street_length, time_serie):
    meters = street_length
    serie = []
    serie.append(meters)
    for i in range(1, len(time_serie)):
        if time_serie[i] > time_serie[i - 1]:
            span = abs(time_serie[i] - time_serie[i - 1])
            meters = meters + (street_length * span)
        serie.append(meters)
    serie = np.array(serie) / 1000
    return meters / 1000

def average_vehicles_track(time_serie):
    return np.mean(time_serie)

def calcPercentaceOfTracks(data, time_series_labels, links_info):
    i = 0
    cluster_percentage = 0
    for xx in data:
        print('Serie '+str(time_series_labels[i]))
        link_id = time_series_labels[i].split("-")
        link_id = link_id[0]
        link_info = links_info[link_id]
        percentage = percentage_of_track(link_info[0], xx.ravel())
        percentage = gmean(percentage)
        cluster_percentage = cluster_percentage + percentage
        print('\t-Percentage of Track: '+str(percentage)+"%")
        i = i + 1   
    if i > 0:     
        cluster_percentage = cluster_percentage / i
        print('\t-Cluster Percentage: '+str(cluster_percentage)+"%")

def calcPercentaceOfTrack(time_serie, link_id, links_info):
    link_info = links_info[link_id]
    percentage = percentage_of_track(link_info[0], time_serie)
    #chartSerie(len(percentage), np.array(percentage), "Percentage of track serie: "+str(link_id), link_id, w = 100)
    percentage = np.mean(percentage)
    return percentage

def getAvegareSpeedOfTrack(time_serie, link_id, links_info):
    link_info = links_info[link_id]
    avg_speed = get_average_speed(link_info[0], link_info[2], time_serie)
    #chartSerie(len(avg_speed), np.array(avg_speed), "Average Speed serie: "+str(link_id), link_id, w = 100)
    avg_speed = gmean(avg_speed)
    return avg_speed

def calcAverageSpeed(data, time_series_labels, links_info):
    i = 0
    cluster_average_speed = 0
    for xx in data:
        print('Serie '+str(time_series_labels[i]))
        link_id = time_series_labels[i].split("-")
        link_id = link_id[0]
        link_info = links_info[link_id]
        avg_speed = get_average_speed(link_info[0], link_info[2], xx.ravel())
        avg_speed = np.sum(avg_speed) / len(avg_speed)
        cluster_average_speed = cluster_average_speed + avg_speed
        print('\t-Average Speed: '+str(avg_speed))
        i = i + 1        
    if i > 0:
      cluster_average_speed = cluster_average_speed / i
      print('\t-Cluster Average Speed: '+str(cluster_average_speed))