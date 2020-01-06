import scripts2.fits_image as fits_image
from scripts2.binning_methods import WvtBinning
#import scripts2.spectral_analysis as spec
#import scripts2.spectral_fitting as spec_fit

import time
import os
import sys
import multiprocessing

"""
kwargs = {'image_name': 'A2554.img',
          'object_name': 'A2554 Galaxy Cluster',
          'center': [182, 178],
          'filter_type': 'circle',
          'filter_args': ([187, 182], 100),
          'target_sn': 20}

kwargs = {'image_name': 'A2554.img',
          'object_name': 'A2554 Galaxy Cluster',
          'center': [182, 178],
          'filter_type': 'poly',
          'filter_args': ([7, 166], [168, 363], [365, 201], [200, 5]),
          'target_sn': 10}

kwargs = {'image_name': 'A1589.fits',
          'object_name': 'A1589 Galaxy Cluster',
          'center': [655, 638],
          'filter_type': 'circle',
          'filter_args': ([655, 638], 140),
          'target_sn': 20}

kwargs = {'image_name': 'A3693.fits',
          'object_name': 'A3693 Galaxy Cluster',
          'center': [701, 683],
          'filter_type': 'poly',
          'filter_args': ([490, 570], [588, 875], [890, 776], [792, 471]),
          'target_sn': 35}

kwargs = {'image_name': 'A2667.img',
          'object_name': 'A2667 Galaxy Cluster',
          'center': [259, 224],
          'filter_type': 'poly',
          'filter_args': ([175, 175], [265, 401], [383, 360], [290, 126]),
          'target_sn': 35}

kwargs = {'image_name': 'A2667.img',
          'object_name': 'A2667 Galaxy Cluster',
          'center': [259, 224],
          'filter_type': 'circle',
          'filter_args': ([259, 224], 200),
          'target_sn': 35}
"""
kwargs = {'image_name': 'adapt-400-7200-nps.fits',
          'object_name': 'A2667 Galaxy Cluster (xmm)',
          'center': [259, 224],
          'filter_type': 'circle',
          'filter_args': ([207.66, 213.7], 120),
          'target_sn': 130}


def binning(iter=40):
    # Part 1 -----> Binning
    starting_time = time.time()

    img = fits_image.FitsImage(kwargs)

    img.open_image()
    img.filter_image()
    img.calculate_sn()
    # img.display()

    wvt = WvtBinning(img)
    wvt.generate_bins()
    wvt.share_pixels()
    wvt.move_to_centroid(iter)
    wvt.save_outputs()
    #wvt.save_bins_as_region_file()

    ending_time = time.time()
    execution_time_sec = ending_time - starting_time
    execution_time_min = execution_time_sec / 60.0
    execution_time_milisec = execution_time_sec * 1000.0

    if 1 <= execution_time_sec < 60:
        print('Execution time: %.2f seconds' % execution_time_sec)
    elif execution_time_sec < 1:
        print('Execution time: %.2f miliseconds' % execution_time_milisec)
    else:
        print('Execution time: %.2f minutes' % execution_time_min)

    wvt.make_plots()

    wvt.change_pixel_values_sur_bri()
    img.save_image('sur_bri.fits')
    wvt.change_pixel_values_number()
    img.save_image('number.fits')
    img.display()

"""
def extract_spectrum():
    event_path = os.path.join(os.getcwd(),'event_file')
    region_path = os.path.join(os.getcwd(),'regions')
    spec.copy_region_files(region_path,event_path)

    event_file = input("Event File Name: ")
    if not event_file:
        event_file = 'evt2_clean.fits'
    event_file_path = os.path.join(event_path,event_file)

    bkg_file = input("Background File Name: ")
    if not bkg_file:
        bkg_file = 'blanksky.fits'
    bkg_file_path = os.path.join(event_path,bkg_file)

    jobs = []

    os.chdir(event_path)

    i = 1
    n = 5

    for i in range(i,n+1):
        p = multiprocessing.Process(target=spec.spectrum, args=(i,n,event_file_path,bkg_file_path))
        jobs.append(p)
        p.start()

def fit_spectrum():
    i = 1
    n = 5
    spec_fit.fit(i,n)
"""
binning(iter=20)
#extract_spectrum()
#fit_spectrum()
