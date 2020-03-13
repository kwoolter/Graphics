import copy
import random
import numpy as np


class World3D:

    INVERSE = np.array([-1, -1, -1])
    NORTH = np.array([0,0,1])
    SOUTH = np.multiply(NORTH, INVERSE)
    EAST = np.array([1,0,0])
    WEST = np.multiply(EAST, INVERSE)
    UP = np.array([0,1,0])
    DOWN = np.multiply(UP, INVERSE)

    HEADINGS = (NORTH, SOUTH, EAST, WEST, UP, DOWN)

    def __init__(self, w, h, d):

        self.width = w
        self.height = h
        self.depth = d

        self.objects = []

    def add_object(self, new_object, x, y, z):

        if self.is_valid_xyz(x,y,z) is True:

            self.objects.append(((x,y,z),copy.deepcopy(new_object)))

    def is_valid_xyz(self,x,y,z):

        if x < 0 or x > self.width or y <0 or y > self.height or z <0 or z > self.depth:
            return False
        else:
            return True

    def build(self, obj_count = 500):

        for i in range(1, obj_count):
            new_object = Object3D(random.randint(1, 3),
                                  random.randint(1, 5),
                                  random.choice(World3D.HEADINGS))

            self.add_object(new_object, random.randint(0, 1000), random.randint(0, 1000),
                            random.randint(0, 1000))

        for i in range(30,200):
            new_object = Object3D(1, 1, random.choice(World3D.HEADINGS))

            self.add_object(new_object, 500, 100, i)

    def print(self):
        print("Headings {0}".format(World3D.HEADINGS))
        for pos, obj in self.objects:
            print("{0}:{1}".format(pos,obj))


class Object3D:

    def __init__(self, type, size = 1, facing = World3D.NORTH):
        self.type = type
        self.size = size
        self.facing = facing

    def __str__(self):
        return "type({0})".format(self.type)