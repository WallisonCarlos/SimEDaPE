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

def pruning(list_to_prune):
    return [0 if i < 0 else i for i in list_to_prune]

def up_shift(list_to_shift):
    min_element = min(list_to_shift)
    if min_element < 0:
        return np.array(list_to_shift) + abs(min_element)
    else:
        return list_to_shift