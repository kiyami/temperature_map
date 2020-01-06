import random as rnd

import scripts2.bin_class as bc
import scripts2.general_methods as gm


class WvtBinning:
    def __init__(self, image):
        self.image = image

        self.bin_number = 1
        self.bin_list = []

        self.power_of_delta = 0.6

    def start_binning(self):
        print('Binning started!')
        print('Input args')
        for key in self.image.kwargs.keys():
            print(key, self.image.kwargs[key])

    def generate_bins(self, number=None):
        if not number:
            self.bin_number = int(self.image.signal / (self.image.target_sn ** 2.0))
        else:
            self.bin_number = number

        temp = []
        counter = 1
        for i in range(self.bin_number):
            generated = False
            while not generated:
                x, y = rnd.choice(self.image.filtered_pixels)
                if not ([x, y] in temp):
                    self.bin_list.append(bc.WvtBin(self, [x, y], counter))
                    temp.append([x, y])
                    generated = True
                    counter += 1
                    print("Bin "+str(len(self.bin_list))+" generated")

    def share_pixels(self):
        for single_bin in self.bin_list:
            single_bin.pixel_list = list()

        for pixel in self.image.filtered_pixels:
            temp_distance = []

            for single_bin in self.bin_list:
                temp_distance.append((gm.distance(single_bin.bin_center, pixel))/(single_bin.delta**self.power_of_delta))

            index = temp_distance.index(min(temp_distance))
            self.bin_list[index].add_pixel(list(pixel))

        for single_bin in self.bin_list:
            single_bin.calculate_sn()
            single_bin.calculate_delta()

    def change_pixel_values_sur_bri(self):
        for single_bin in self.bin_list:
            signal = float(single_bin.signal)
            area = float(single_bin.area)
            value = signal/area
            for pixel in single_bin.pixel_list:
                self.image.modified_image_data[pixel[1], pixel[0]] = value

    def change_pixel_values_number(self):
        for single_bin in self.bin_list:
            for pixel in single_bin.pixel_list:
                self.image.modified_image_data[pixel[1], pixel[0]] = int(single_bin.bin_name)

    def move_to_centroid(self, iteration=1):
        for j in range(iteration):
            for single_bin in self.bin_list:
                single_bin.calculate_centroid()
                single_bin.bin_center = list(single_bin.centroid)
            self.share_pixels()
            print(str(j+1)+". iteration!")

    def save_outputs(self):
        with open('sn.txt', 'w') as text_file:
            for single_bin in self.bin_list:
                sn = float(single_bin.sn)
                area = float(single_bin.area)
                radius = float(gm.distance(self.image.center, single_bin.bin_center))
                text_file.write("%f %f %f \n" % (sn, area, radius))

    def save_bins_as_region_file(self):
        gm.clear_folder('regions')

        for single_bin in self.bin_list:
            single_bin.sort_coordinates()
            single_bin.save_bin_as_region_file()
            print('Region %s created' % single_bin.bin_name)

    @staticmethod
    def make_plots():
        gm.plot_area('sn.txt')
        gm.plot_sn('sn.txt')


class ContourBinning:
    def __init__(self):
        pass


class SomeBinningMethod:
    def __init__(self):
        pass
