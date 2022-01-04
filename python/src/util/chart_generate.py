import matplotlib.pylab as plt

def average(array, init, end):
    s = 0
    if end >= len(array):
        end = len(array) -1
    for i in array[init:end]:
        s = s + i
    if (end - init) > 0:
        return s / (end - init)
    else:
        return s

def avegare_movable(array, w):
    newarray = list()
    for i in range(len(array)):
        newarray.append(average(array, i, i + w))
    return newarray

def revert_data(data, std, mean):
    data = (data  * std) + mean
    return data

def plot_serie(size_x, time_series, legend, title, avegare_movable = 100, color = 'g-', x_label = 'Simulation time step', y_label = 'Number of vehicles on the track', save = False, file_name = 'time_series.png'):
    plt.plot(avegare_movable(time_series.ravel(), avegare_movable), color)
    plt.xlim(0, size_x)
    plt.text(0.55, 0.85,'%s' % legend,
             title=plt.gca().transAxes)
    plt.title(title)
    plt.tight_layout()
    if save:
        plt.savefig(file_name)
    plt.show()