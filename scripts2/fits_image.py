from astropy.io import fits
from astropy import wcs
from astropy.coordinates import SkyCoord
from astropy import units as u

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np

import scripts2.general_methods as gm
import scripts2.polygon_class as pc


class FitsImage:
    def __init__(self, kwargs):
        self.kwargs = kwargs

        self.image_name = self.kwargs['image_name']
        self.object_name = self.kwargs['object_name']
        self.center = self.kwargs['center']
        self.filter_type = self.kwargs['filter_type']
        self.filter_args = self.kwargs['filter_args']
        self.target_sn = self.kwargs['target_sn']

        self.image_data = None
        self.modified_image_data = None
        self.wcs_data = None
        self.shape = []

        self.filtered_pixels = []
        self.filtered_pixel_values = []

        self.signal = 1.0
        self.noise = 1.0
        self.sn = 1.0

        print('Fits image initialized!')

    def open_image(self):
        with fits.open(self.image_name) as hdu_list:
            hdu_list[0].scale('float32')
            self.image_data = hdu_list[0].data
            self.wcs_data = wcs.WCS(hdu_list[0].header)
            self.shape = [self.image_data.shape[1], self.image_data.shape[0]]

        self.modified_image_data = self.image_data.copy()

    def save_image(self, new_name=''):
        if not new_name:
            new_name = 'new_image.fits'

        with fits.open(self.image_name) as hdu_list:
            hdu_list[0].scale('float32')
            hdu_list[0].data = self.modified_image_data
            hdu_list.writeto(new_name, overwrite=True)

    def display(self, original_data=False):
        fig, ax = plt.subplots(1)
        ax.set_aspect('equal')
        if original_data:
            ax.imshow(self.image_data, cmap='gray', norm=LogNorm())
        else:
            ax.imshow(self.modified_image_data, cmap='gray', norm=LogNorm())
        ax_rev = plt.axis()
        plt.axis((ax_rev[0], ax_rev[1], ax_rev[3], ax_rev[2]))
        plt.show()

    def filter_image(self):
        if self.filter_type == 'circle':
            self.filter_circle()
        elif self.filter_type == 'poly':
            self.filter_poly()
        elif self.filter_type == 'value':
            self.filter_value()
        else:
            self.filter_default()

    def filter_circle(self):
        x, y = self.filter_args[0]
        radius = self.filter_args[1]

        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if gm.distance([x, y], [i, j]) <= radius:
                    self.filtered_pixels.append([i, j])
                    self.filtered_pixel_values.append(self.modified_image_data[j, i])
                else:
                    self.modified_image_data[j, i] = 0

    def filter_poly(self):  # may need improvement
        poly = pc.Polygon(self.filter_args)
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if poly.inside([i, j]):
                    self.filtered_pixels.append([i, j])
                    self.filtered_pixel_values.append(self.modified_image_data[j, i])
                else:
                    self.modified_image_data[j, i] = 0

    def filter_value(self):
        pass

    def filter_default(self):
        pass

    def calculate_sn(self):
        signal = 0
        sn = 0
        for value in self.filtered_pixel_values:
            signal += value
        noise = signal**0.5
        if noise:
            sn = signal/noise

        self.signal = signal
        self.noise = noise
        self.sn = sn

    def pixel_to_fk5(self, pixel):
        x, y = pixel
        pixcrd = np.array([[x + 1, y + 1]], np.float_)
        world = self.wcs_data.wcs_pix2world(pixcrd, 1)

        ra_w = world[0, 0]
        dec_w = world[0, 1]

        sky = SkyCoord(ra=ra_w * u.degree, dec=dec_w * u.degree)
        sky = sky.fk5
        sky = sky.to_string('hmsdms')
        sky_ra, sky_dec = sky.split(" ")
        sky_ra = sky_ra.replace("h", ":")
        sky_ra = sky_ra.replace("m", ":")
        sky_ra = sky_ra.replace("s", "")
        sky_dec = sky_dec.replace("d", ":")
        sky_dec = sky_dec.replace("m", ":")
        sky_dec = sky_dec.replace("s", "")

        return sky_ra, sky_dec
