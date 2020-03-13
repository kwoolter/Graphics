import pygame
import os
from pygame.locals import *
import math
import numpy as np
import random
import model3d as model


class Colours:
    # set up the colours
    BLACK = (0, 0, 0)
    BROWN = (128, 64, 0)
    WHITE = (255, 255, 255)
    RED = (237, 28, 36)
    GREEN = (34, 177, 76)
    BLUE = (63, 72, 204)
    DARK_GREY = (40, 40, 40)
    GREY = (128, 128, 128)
    GOLD = (255, 201, 14)
    YELLOW = (255, 255, 0)
    TRANSPARENT = (255, 1, 1)

    @staticmethod
    def scale(colour, factor):
        r, g, b = colour
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        return (r, g, b)

    @staticmethod
    def rgb_to_greyscale(colour):
        r, g, b = colour

        c = min(int(math.sqrt(r * r + g * g + b * b)), 255)

        return (c, c, c)


class BaseView():

    def __init__(self, width: int = 0, height: int = 0):
        self.tick_count = 0
        self.height = height
        self.width = width
        self.surface = None

    def initialise(self):
        pass

    def tick(self):
        self.tick_count += 1

    def draw(self):
        pass


class MainFrame(BaseView):
    RESOURCES_DIR = os.path.dirname(__file__) + "\\resources\\"

    COLOURS = [Colours.RED, Colours.GREEN, Colours.GOLD, Colours.BLUE]

    def __init__(self, width: int = 800, height: int = 800):

        super(MainFrame, self).__init__(width, height)

        self.fill_colour = Colours.WHITE

        self.view_pos = (500, 500, 0)
        self.view_width = 1000
        self.view_height = 1000
        self.view_depth = 200
        self.object_size_scale = 4
        self.object_distance_scale = 1000

        self.model = None
        self.m2v = None

    def initialise(self):

        super(MainFrame, self).initialise()

        # pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF | pygame.HWACCEL)
        # self.surface = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        self.surface = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF | pygame.HWACCEL)

        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        pygame.display.set_caption("3D Space")
        filename = MainFrame.RESOURCES_DIR + "icon.png"

        try:
            image = pygame.image.load(filename)
            image = pygame.transform.scale(image, (32, 32))
            pygame.display.set_icon(image)
        except Exception as err:
            print(str(err))

        self.model = model.World3D(1000, 1000, 2000)

        self.model.build(1000)

        # self.model.print()

        self.m2v = ModelToView3D(self.model)

    def draw(self):

        # super(MainFrame, self).draw(self)

        self.surface.fill(Colours.BLACK)
        vx, vy, vz = self.view_pos

        objs = self.m2v.get_object_list(self.view_pos, self.view_width, self.view_height, self.view_depth)

        distance = sorted(list(objs.keys()), reverse=True)
        for d in distance:
            objs_at_d = objs[d]
            for pos, obj in objs_at_d:
                x, y, z = pos
                if d > 0:
                    size = int(obj.size * self.object_size_scale * (1 - d / self.object_distance_scale))
                    # size = int(obj.size * self.object_size_scale / d)
                    pygame.draw.rect(self.surface, Colours.rgb_to_greyscale(MainFrame.COLOURS[obj.type]),
                                     (x - int(size / 2), y - int(size / 2), size, size))
                    # pygame.draw.rect(self.surface, MainFrame.COLOURS[obj.type], (x, y, 10,10))
                    # pygame.draw.rect(self.surface, MainFrame.COLOURS[obj.type], (10,10, 10, 10))

                # print("[{0}:{1}".format(pos,obj))

        pygame.draw.circle(self.surface, Colours.RED, (int(self.view_width / 2), int(self.view_height / 2)), 10, 1)

    def tick(self):

        # self.fill_colour = Colours.scale(self.fill_colour, 0.95)

        self.view_pos = np.add(self.view_pos, np.array(model.World3D.NORTH))

        x, y, z = self.view_pos

        if z > self.model.depth:
            self.view_pos = np.multiply(self.view_pos, np.array([1, 1, 0]))
            print("Going back to z = 0: {0}".format(self.view_pos))

        return

    def update(self):
        pygame.display.update()

    def end(self):
        pygame.quit()


def main():
    obj_size = 10
    object_size_scale = 1
    object_distance_scale = 100

    for d in range(100, 0, -1):
        view_size = int(obj_size * object_size_scale * (1 - (d / object_distance_scale)))
        print(d, view_size)

    pygame.init()

    view = MainFrame(width=1000, height=1000)
    view.initialise()

    os.environ["SDL_VIDEO_CENTERED"] = "1"

    FPSCLOCK = pygame.time.Clock()

    pygame.time.set_timer(USEREVENT + 1, 10)
    pygame.time.set_timer(USEREVENT + 2, 500)
    pygame.event.set_allowed([QUIT, KEYUP, USEREVENT])

    loop = True

    while loop is True:

        # Loop to process pygame events
        for event in pygame.event.get():

            # Process 1 second timer events
            if event.type == USEREVENT + 1:

                view.tick()

                try:
                    pass

                except Exception as err:
                    print(str(err))

            # Process 0.5 second timer events
            elif event.type == USEREVENT + 2:
                pass

            # Key pressed events
            elif event.type == KEYDOWN:
                if event.key in (K_UP, K_w):
                    view.view_pos = np.add(view.view_pos, np.array(model.World3D.NORTH))
                elif event.key in (K_DOWN, K_s):
                    view.view_pos = np.add(view.view_pos, np.array(model.World3D.SOUTH))
                elif event.key in (K_LEFT, K_a):
                    view.view_pos = np.add(view.view_pos, np.array(model.World3D.WEST))
                elif event.key in (K_RIGHT, K_d):
                    view.view_pos = np.add(view.view_pos, np.array(model.World3D.EAST))
                elif event.key in (K_q, K_q):
                    view.view_pos = np.add(view.view_pos, np.array(model.World3D.UP))
                elif event.key in (K_e, K_e):
                    view.view_pos = np.add(view.view_pos, np.array(model.World3D.DOWN))
                print(view.view_pos)


            # QUIT event
            elif event.type == QUIT:
                loop = False
        try:
            view.draw()
            view.update()
        except Exception as err:
            print(str(err))

        FPSCLOCK.tick(50)

    view.end()

    return 0


class ModelToView3D():

    def __init__(self, model):
        self.model = model

        self.infinity = 1000

    def get_object_list(self, view_pos, view_width, view_height, view_depth, view_heading=model.World3D.NORTH):
        objects = {}

        vx, vy, vz = view_pos

        for (ox, oy, oz), obj in self.model.objects:

            od = oz - vz
            ow = ox - vx
            oh = oy - vy

            if od < 0 or od > view_depth or abs(ow) > view_width / 2 or abs(oh) > view_height / 2:
                pass
            else:

                # If we don't have a list of objects at this distance then create an empty one
                if od not in objects.keys():
                    objects[od] = []

                # Add ((x,y,z), obj)) to list of objects at this distance
                objects[od].append((
                    ((ow * (1 - od / self.infinity)) + int(view_width / 2),
                     (oh * (1 - od / self.infinity)) + int(view_height / 2),
                     od), obj))

        return objects


if __name__ == "__main__":
    main()
