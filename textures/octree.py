from math import sqrt
from collections import namedtuple
from PIL import Image


def cut_pallet(image, colors_left):
    tree = OctTree()
    for red, green, blue in image.getdata():
        tree.add_color(red, green, blue)
    tree.delete_nodes(colors_left)
    pallet = []
    tree.build_pallet(pallet)
    return pallet


def get_bit(number, bit_number):
    mask = 1 << bit_number
    if number & mask > 0:
        return 1
    else:
        return 0

color_tuple = namedtuple('color', ['red', 'green', 'blue'])


def closest_color_from_pallet(pallet, array_color):
    color = color_tuple(array_color[0], array_color[1], array_color[2])
    new_color = min(
        (color_pallet for color_pallet in pallet),
        key=lambda x: color_length(x, color)
    )
    return new_color.red, new_color.green, new_color.blue


def color_length(color1, color2):
    return sqrt(
        (color1.red - color2.red) * (color1.red - color2.red) +
        (color1.green - color2.green) * (color1.green - color2.green) +
        (color1.blue - color2.blue) * (color1.blue - color2.blue)
    )


class OctTree(object):
    def __init__(self):
        self.root = Node(None)
        self.color_count = 0

    def add_color(self, red, green, blue):
        actual_node = self.root
        for i in range(8):
            l = get_bit(red, i) + get_bit(green, i) * 2 + get_bit(blue, i) * 4
            if actual_node.children[l] is None:
                actual_node.children[l] = Node(actual_node)
                actual_node = actual_node.children[l]
                if i == 7:
                    self.color_count += 1
            else:
                actual_node = actual_node.children[l]
            actual_node.color_count += 1
        actual_node.red, actual_node.green, actual_node.blue = red, green, blue
        actual_node.leaf_color_count += 1

    def delete_nodes(self, color_left):
        while self.color_count >= color_left:
            node = self._find_minimum_leaf()
            counter = 0
            for child in node.parent.children:
                if child is not None:
                    counter += 1
            if counter >= 2:
                self.color_count -= 1
            self._delete_leaf(node)


    def build_pallet(self, pallet, actual_node=None):
        if actual_node is None:
            actual_node = self.root
        if actual_node.children is not None and max(actual_node.children) is None:
            pallet.append(
                color_tuple(actual_node.red, actual_node.green, actual_node.blue)
            )
            return
        for node in actual_node.children:
            if node is not None:
                self.build_pallet(pallet, actual_node=node)

    def _find_minimum_leaf(self):
        min_node = self.root
        while min_node is not None:
            actual_node = min_node
            min_node = None
            for node in actual_node.children:
                if min_node is None and node is not None:
                    min_node = node
                elif (
                    min_node is not None and node is not None and
                    node.color_count < min_node.color_count
                ):
                    min_node = node
        return actual_node

    def _delete_leaf(self, node):
        parent = node.parent
        leaf_color_count = parent.leaf_color_count + node.leaf_color_count
        if parent.red is None:
            parent.red = node.red
            parent.blue = node.blue
            parent.green = node.green
        else:
            parent.red = (
                parent.leaf_color_count * parent.red +
                node.leaf_color_count * node.red
            ) / leaf_color_count

            parent.green = (
                parent.leaf_color_count * parent.green +
                node.leaf_color_count * node.green
            ) / leaf_color_count

            parent.blue = (
                parent.leaf_color_count * parent.blue +
                node.leaf_color_count * node.blue
            ) / leaf_color_count

        parent.leaf_color_count = leaf_color_count
        index = parent.children.index(node)
        parent.children[index] = None


class Node(object):

    def __init__(self, parent, red=None, green=None, blue=None):
        self.red = red
        self.green = green
        self.blue = blue
        self.color_count = 0
        self.leaf_color_count = 0
        self.parent = parent
        self.children = [None for _ in range(8)]
