import time
import sys

sys.path.append('scaler')

from scaler.TimeSeriesScalerSimEDaPE import TimeSeriesScalerSimEDaPE
from tslearn.clustering import KShape
from tslearn.datasets import CachedDatasets
from tslearn.preprocessing import TimeSeriesResampler
from tslearn.utils import to_time_series_dataset
import numpy as np
import math

def proccess_dataset(data, size):
    print("Processing dataset...")
    X = to_time_series_dataset(data)
    X = TimeSeriesResampler(int(size)).fit_transform(X)
    X, mean, std = TimeSeriesScalerSimEDaPE().fit_transform(X)
    print("Dataset process finished!")
    return X, mean, std

def clustering(data, n_clusters = 36, verbose = True, random_state = 10, max_iter = 8):
    print("Clustering...")
    ks = KShape(n_clusters = n_clusters, verbose= verbose, random_state = random_state, max_iter= max_iter)
    start_time = time.time()
    if verbose:
        print(start_time)
    y_pred = ks.fit_predict(data)
    end_time = time.time()
    if verbose:
        print(end_time)
        print(end_time - start_time)
    print("Clustering finished!")
    return ks, y_pred

def time_series_labels_indexs(time_series_labels):
    time_series_labels_indexs = []
    for i in range(len(time_series_labels)):
        time_series_labels_indexs.append(i)
    return time_series_labels_indexs

def simulation_points_indexs(clustering, time_series_labels_indexs, X):
    time_series_labels_indexs = np.array(time_series_labels_indexs)
    simulation_points_indexs = []
    for k in range(clustering['number_of_clusters']):
        cen =  np.array(clustering['centroids'][str(k)]).ravel()
        index = -1
        smallest = 1000000000
        for i in time_series_labels_indexs[np.array(clustering['clusters']) == k]:
            error = np.sum(np.abs(cen - X[i].ravel()))
            if error < smallest:
                smallest = error
            index = i   
        simulation_points_indexs.append(index)
    return simulation_points_indexs

def simulation_points_labels(time_series_labels, simulation_points_indexs):
    simulation_points_labels = []
    for i in simulation_points_indexs:
        simulation_points_labels.append(time_series_labels[i].split('-')[0])
    return simulation_points_labels

def silumlation_points_vehicles(street_vehicles, simulation_points_labels):
    silumlation_points_vehicles = {}
    for simulation_point_label in simulation_points_labels:
        silumlation_points_vehicles[simulation_point_label] = []
        for time_series_vehicles in street_vehicles[simulation_point_label]:
            for vehicle in time_series_vehicles:
                if not vehicle in silumlation_points_vehicles[simulation_point_label]:
                    silumlation_points_vehicles[simulation_point_label].append(vehicle)
    return silumlation_points_vehicles

def warping_paths(s1, s2, window=None, max_dist=None,
                  max_step=None, max_length_diff=None, penalty=None, psi=None):
    """
    Dynamic Time Warping.
    The full matrix of all warping paths is build.
    :param s1: First sequence
    :param s2: Second sequence
    :param window: see :meth:`distance`
    :param max_dist: see :meth:`distance`
    :param max_step: see :meth:`distance`
    :param max_length_diff: see :meth:`distance`
    :param penalty: see :meth:`distance`
    :param psi: see :meth:`distance`
    :returns: (DTW distance, DTW matrix)
    """
    r, c = len(s1), len(s2)
    if max_length_diff is not None and abs(r - c) > max_length_diff:
        return np.inf
    if window is None:
        window = max(r, c)
    if not max_step:
        max_step = np.inf
    else:
        max_step *= max_step
    if not max_dist:
        max_dist = np.inf
    else:
        max_dist *= max_dist
    if not penalty:
        penalty = 0
    else:
        penalty *= penalty
    if psi is None:
        psi = 0
    dtw = np.full((r + 1, c + 1), np.inf)
    for i in range(psi + 1):
        dtw[0, i] = 0
        dtw[i, 0] = 0
    last_under_max_dist = 0
    i0 = 1
    i1 = 0
    for i in range(r):
        if last_under_max_dist == -1:
            prev_last_under_max_dist = np.inf
        else:
            prev_last_under_max_dist = last_under_max_dist
        last_under_max_dist = -1
        i0 = i
        i1 = i + 1
        for j in range(max(0, i - max(0, r - c) - window + 1), min(c, i + max(0, c - r) + window)):
            d = (s1[i] - s2[j])**2
            if max_step is not None and d > max_step:
                continue
            dtw[i1, j + 1] = d + min(dtw[i0, j],
                                     dtw[i0, j + 1] + penalty,
                                     dtw[i1, j] + penalty)
            if max_dist is not None:
                if dtw[i1, j + 1] <= max_dist:
                    last_under_max_dist = j
                else:
                    dtw[i1, j + 1] = np.inf
                    if prev_last_under_max_dist < j + 1:
                        break
        if max_dist is not None and last_under_max_dist == -1:
            return np.inf, dtw
    dtw = np.sqrt(dtw)
    if psi == 0:
        d = dtw[i1, min(c, c + window - 1)]
    else:
        ir = i1
        ic = min(c, c + window - 1)
        vr = dtw[ir-psi:ir+1, ic]
        vc = dtw[ir, ic-psi:ic+1]
        mir = np.argmin(vr)
        mic = np.argmin(vc)
        if vr[mir] < vc[mic]:
            dtw[ir-psi+mir+1:ir+1, ic] = -1
            d = vr[mir]
        else:
            dtw[ir, ic - psi + mic + 1:ic+1] = -1
            d = vc[mic]
    return d, dtw

def best_path(paths, x1, x2):
    """Compute the optimal path from the nxm warping paths matrix."""
    i, j = int(paths.shape[0] - 1), int(paths.shape[1] - 1)
    p = []
    if paths[i, j] != -1:
        fun = 0
        if (x1[i-1] > x2[j-1]):
            fun = 1
        p.append((i - 1, j - 1, paths[i, j], fun))
    while i > 0 and j > 0:
        c = np.argmin([paths[i - 1, j - 1], paths[i - 1, j], paths[i, j - 1]])
        if c == 0:
            i, j = i - 1, j - 1
        elif c == 1:
            i = i - 1
        elif c == 2:
            j = j - 1
        if paths[i, j] != -1:
            fun = 0
            if (x1[i-1] > x2[j-1]):
                fun = 1
            p.append((i - 1, j - 1, paths[i, j], fun))
    p.pop()
    p.reverse()
    return p

def get_warping_path(ts_1, ts_2):
    d, paths = warping_paths(ts_1, ts_2, window = math.floor(len(ts_2) * 0.10))
    bp = best_path(paths, ts_1, ts_2)
    return bp, d

def warping_path_calculation(clustering, time_series_labels_indexs, data):
    time_series_labels_indexs = np.array(time_series_labels_indexs)
    start_time = time.time()
    print(start_time)
    wps = {}
    wps['number_of_clusters'] = clustering['number_of_clusters'] 
    wps['warping_paths'] = {}
    for k in range(clustering['number_of_clusters']):
        cen =  np.array(clustering['centroids'][str(k)]).ravel()
        wps['warping_paths'][str(k)] = {}
        print("Cluster: ", k)
        for i in time_series_labels_indexs[np.array(clustering['clusters']) == k]:
            s = data[i].ravel()
            warping_path, d = get_warping_path(cen, s)
            wps['warping_paths'][str(k)][str(i)] = warping_path
    end_time = time.time()
    print(end_time)
    print("Time execution", end_time - start_time)
    return wps