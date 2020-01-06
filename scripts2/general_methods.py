import os
import sys

import matplotlib.pyplot as plt
from numpy import loadtxt


def distance(point_1, point_2):
    x1, y1 = point_1
    x2, y2 = point_2
    return ((x2 - x1)**2.0 + (y2 - y1)**2.0)**0.5


def corners_of_a_pixel(pixel):
    x = pixel[0]
    y = pixel[1]
    return [x-0.5, y-0.5], [x-0.5, y+0.5], [x+0.5, y-0.5], [x+0.5, y+0.5]


def plot_sn(file_name):
    data = loadtxt(file_name)
    sn = data[:, 0]
    radius = data[:, 2]

    n = len(sn)
    mean = sum(sn) / n
    temp = [(x - mean) ** 2.0 for x in sn]
    std = (sum(temp) / n) ** 0.5
    y_max = 2.0 * sum(sn) / n

    plt.clf()

    plt.scatter(radius, sn, label='Bins')
    plt.xlim(0, max(radius))
    plt.ylim(0, 1.2 * y_max)
    plt.xlabel('Radius (Pixel)')
    plt.ylabel('S/N')

    plt.title(r'$\mathrm{Distribution\ of\ S/N:}\ \mu=%.2f,\ \sigma=%.2f$' % (mean, std))
    plt.grid(True)

    plt.axhline(y=mean, color='red', linewidth=3, label='Mean')
    plt.axhline(y=mean + std, color='red', linestyle='dashed', linewidth=2, label='Std')
    plt.axhline(y=mean - std, color='red', linestyle='dashed', linewidth=2)
    plt.legend()

    outplot = 'sn_distribution.png'
    plt.savefig(outplot)


def plot_area(file_name):
    data = loadtxt(file_name)
    area = data[:, 1]
    radius = data[:, 2]

    sum_area = sum(area)
    area = [x/sum_area for x in area]
    y_max = max(area)

    plt.clf()

    plt.scatter(radius, area, label='Bins')
    plt.xlim(0, max(radius))
    plt.ylim(0, 1.2 * y_max)
    plt.xlabel('Radius (Pixel)')
    plt.ylabel('Area (Ratio)')

    plt.title('Distribution of Bin Area')
    plt.grid(True)

    outplot = 'area_distribution.png'
    plt.savefig(outplot)


def clear_folder(path):
    contents = os.listdir(path)
    path_list = [os.path.join(path, content) for content in contents]
    for single_file in path_list:
        os.remove(single_file)
