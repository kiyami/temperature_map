from ciao_contrib.runtool import *
import timeit
import multiprocessing
import os
import sys
import shutil

print("Number of cpu : ", multiprocessing.cpu_count())

i = 1
n = 5
bin_number = 1

def spectrum(i,n,event_file,bkg_file):
    start = timeit.default_timer()
    print(str(i)+"/"+str(n)+". spectrum started!")
    specextract.punlearn()
    specextract.infile=str(event_file)+"[sky=region(reg-"+str(i)+".reg)]"
    specextract.bkgfile=str(bkg_file)+"[sky=region(reg-"+str(i)+".reg)]"
    specextract.outroot="reg-"+str(i)
    specextract.correctpsf="yes"
    specextract.weight="no"
    specextract.grouptype="NUM_CTS"
    specextract.binspec=bin_number
    specextract.clobber="yes"
    specextract.bkgresp="no"
    specextract()
    stop = timeit.default_timer()
    print("Time of "+str(i)+". spectrum: ", stop - start)


def copy_region_files(region_path,event_path):
    region_files = os.listdir(region_path)
    for file_name in region_files:
        full_file_name = os.path.join(region_path, file_name)
        if (os.path.isfile(full_file_name)):
            shutil.copy(full_file_name, event_path)


if __name__ == '__main__':

    event_path = os.path.join(os.getcwd(),'event_file')
    region_path = os.path.join(os.getcwd(),'regions')

    os.chdir(event_path)
    copy_region_files(region_path,event_path)

    event_file = raw_input("Event File Name: ")
    if not event_file:
        event_file = 'evt2_clean.fits'

    bkg_file = raw_input("Background File Name: ")
    if not bkg_file:
        bkg_file = 'blanksky.fits'

    jobs = []

    for i in range(i,n+1):
        p = multiprocessing.Process(target=spectrum, args=(i,n,event_file,bkg_file))
        jobs.append(p)
        p.start()
