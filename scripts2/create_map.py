from astropy.io import fits
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy import wcs
from astropy.coordinates import Angle
from astropy.coordinates import FK5
import numpy as np
import os
import sys

# integer sorunu scale() fonksiyonu ile cozuldu

class MakeMap():

    def __init__(self,name,txt):
        self.name = name
        self.N = 58
        self.txt = txt
        self.open_image()

    def open_image(self):

        hdu_list = fits.open(self.name)
        hdu_list[0].scale('float32')
        #hdu_list[0].header.update({"bitpix":-32})
        self.image_data = hdu_list[0].data
        """
        self.image_data, header = fits.getdata(self.name, header=True, uint=False)
        header['bitpix'] = -32
        """
        #self.wcs_data = wcs.WCS(hdu_list[0].header)
        self.shape_x = self.image_data.shape[0]
        self.shape_y = self.image_data.shape[1]

        self.read_temp_values()

        for i in range(0,self.shape_x):
            for j in range(0,self.shape_y):
                for k in range(0,self.N):
                    if(self.image_data[i,j]==k+1):
                        self.image_data[i,j] = float(self.temp_values[k])
                        #self.image_data[i,j] = 100.5
        #fits.writeto("temperature_map.fits",self.image_data,header,overwrite=True)
        fits.writeto("temperature_map.fits",self.image_data,hdu_list[0].header,overwrite=True)
        hdu_list.close()


    def read_temp_values(self):
        self.temp_values = []
        with open("fit_outputs.txt") as f:
            content = f.readlines()
            self.N = len(content)
            for line in content:
                kt = line.split(" ")[1]
                self.temp_values.append(kt)

    def read_err_values(self):
        self.temp_err = []
        with open("fit_outputs.txt") as f:
            content = f.readlines()
            for line in content:
                err = line.split(" ")[2]
                err = err[1:-1].split(",")
                err = (float(err[0][1:])+float(err[1][:-1]))/2.0
                self.temp_err.append(err)


if __name__ == '__main__':

    working_directory = os.getcwd()
    output_directory = os.path.join(working_directory,'outputs')

    if os.path.exists(output_directory):
        pass
    else:
        os.mkdir('outputs')

    os.chdir(output_directory)
    a = MakeMap("../number.fits","fit_outputs.txt")
