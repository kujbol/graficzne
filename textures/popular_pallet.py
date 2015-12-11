from collections import OrderedDict
import operator
from textures.octree import color_tuple


def popular_pallet(image, color_count):
    color_dict = dict()
    for red, green, blue in image.getdata():
        try:
            color_dict[red, green, blue] += 1
        except KeyError:
            color_dict[red, green, blue] = 1

    out_list = []
    counter = 0
    iterator = iter(sorted(color_dict.items(), key=operator.itemgetter(1)))

    # hard to use list comprehension
    for color, value in iterator:
        new_color = color_tuple(int(color[0]), int(color[1]), int(color[2]))
        print new_color
        out_list.append(new_color)
        counter += 1
        if counter >= color_count:
            print "done"
            return out_list

