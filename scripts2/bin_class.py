from astropy.io import fits
import scripts2.general_methods as gm
import math


class WvtBin:
    def __init__(self, bin_method, bin_center, bin_name=''):
        self.bin_method = bin_method  # ne ise yariyor
        self.image = self.bin_method.image

        self.bin_name = str(bin_name)
        self.bin_center = bin_center
        self.signal = 1.0
        self.noise = 1.0
        self.sn = 1.0
        self.area = 1.0
        self.delta = 1.0

        self.centroid = []
        self.current_position = []
        self.initial_position = []
        self.pixel_list = []
        self.corner_list = []
        self.border_list = []

        self.current_direction = 0

        self.add_pixel(self.image.center)
        self.calculate_sn()
        self.calculate_centroid()
        self.calculate_delta()

    def add_pixel(self, pixel):
        self.pixel_list.append(pixel)
        self.area = len(self.pixel_list)

    def remove_pixel(self, pixel):
        self.pixel_list.remove(list(pixel))
        self.area = len(self.pixel_list)

    def calculate_sn(self):
        self.signal = 0.0
        for pixel in self.pixel_list:
            self.signal += float(self.image.modified_image_data[pixel[1], pixel[0]])
        self.noise = self.signal**0.5
        if self.noise:
            self.sn = self.signal/self.noise

    def calculate_centroid(self):
        temp_x = 0.0
        temp_y = 0.0

        for pixel in self.pixel_list:
            temp_x += float((pixel[0]-self.bin_center[0])*float(self.image.modified_image_data[pixel[1], pixel[0]]))
            temp_y += float((pixel[1]-self.bin_center[1])*float(self.image.modified_image_data[pixel[1], pixel[0]]))

        if int(self.signal) != 0:
            temp_x = temp_x/float(self.signal)
            temp_y = temp_y/float(self.signal)

        self.centroid = list([temp_x+self.bin_center[0], temp_y+self.bin_center[1]])

    def calculate_delta(self):
        self.delta = ((self.area/math.pi)*(self.image.target_sn/self.sn))**0.5

    def find_corners(self):
        self.corner_list = []
        temp_list = []

        for pixel in self.pixel_list:
            temp_list.extend(gm.corners_of_a_pixel(pixel))

        for i in temp_list:
            if i not in self.corner_list:
                self.corner_list.append(list(i))

    def border_walk(self):
        self.corner_list.sort()
        self.current_position = list(self.corner_list[0])
        self.initial_position = list(self.current_position)
        self.border_list = []

        self.current_direction = 0
        self.border_list.append(list(self.current_position))

        self.move()
        while self.initial_position != self.current_position:
            self.move()

    def can_left(self):
        temp = False
        temp_current = list(self.current_position)
        temp_current[1] -= 1

        for i in self.corner_list:
            if temp_current == i:
                temp = True

        return temp

    def can_up(self):
        temp = False
        temp_current = list(self.current_position)
        temp_current[0] += 1

        for i in self.corner_list:
            if temp_current == i:
                temp = True

        return temp

    def can_right(self):
        temp = False
        temp_current = list(self.current_position)
        temp_current[1] += 1

        for i in self.corner_list:
            if temp_current == i:
                temp = True

        return temp

    def can_down(self):
        temp = False
        temp_current = list(self.current_position)
        temp_current[0] -= 1

        for i in self.corner_list:
            if temp_current == i:
                temp = True

        return temp

    def left(self):
        self.current_position[1] -= 1
        self.current_direction = 0
        self.border_list.append(list(self.current_position))

    def up(self):
        self.current_position[0] += 1
        self.current_direction = 1
        self.border_list.append(list(self.current_position))

    def right(self):
        self.current_position[1] += 1
        self.current_direction = 2
        self.border_list.append(list(self.current_position))

    def down(self):
        self.current_position[0] -= 1
        self.current_direction = 3
        self.border_list.append(list(self.current_position))

    def move(self):
        if self.current_direction == 0:
            if self.can_down():
                self.down()
            elif self.can_left():
                self.left()
            elif self.can_up():
                self.up()
        elif self.current_direction == 1:
            if self.can_left():
                self.left()
            elif self.can_up():
                self.up()
            elif self.can_right():
                self.right()
        elif self.current_direction == 2:
            if self.can_up():
                self.up()
            elif self.can_right():
                self.right()
            elif self.can_down():
                self.down()
        elif self.current_direction == 3:
            if self.can_right():
                self.right()
            elif self.can_down():
                self.down()
            elif self.can_left():
                self.left()
            else:
                print("can not move!")

    def sort_coordinates(self):
        self.find_corners()
        self.border_walk()

    def save_bin_as_region_file(self):
        reg_file_text = '''# Region file format: DS9 version 4.1\nglobal color=green \
dashlist=8 3 width=1 font="helvetica 10 normal roman" select=1 \
highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\n'''

        with open("regions/reg-"+self.bin_name+".reg", "w") as reg_file:
            reg_file.write(reg_file_text)
            reg_file.write("image\npolygon(")

            for j, i in self.border_list:
                ra, dec = self.image.pixel_to_fk5([j, i])
                reg_file.write(str(ra) + "," + str(dec) + ",")

            reg_file.seek(reg_file.tell() - 1, 0)
            reg_file.write(")\n")
