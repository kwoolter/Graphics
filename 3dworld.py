import pygame
import os
from pygame.locals import *
import math
import model3d as model
import numpy as np


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


class spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename)
        except Exception as err:
            print('Unable to load spritesheet image:', filename)
            raise err

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle = None, colorkey = None):
        if rectangle is None:
            rectangle = self.sheet.get_rect()
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, depth=24)
        key = (0, 255, 0)
        image.fill(key)
        image.set_colorkey(key)
        image.blit(self.sheet, (0, 0), rect)

        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

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

    COLOURS = [Colours.RED, Colours.GREEN, Colours.GOLD, Colours.BLUE, Colours.YELLOW, Colours.WHITE]

    def __init__(self, width: int = 800, height: int = 800):

        super(MainFrame, self).__init__(width, height)

        self.fill_colour = Colours.WHITE

        self.view_pos = (500, 500, 0)
        self.view_width = width
        self.view_height = height
        self.view_depth = 250
        self.object_size_scale = 10
        self.object_distance_scale = 400

        self.model = None
        self.m2v = None

        self.alien_images = []

    def initialise(self):

        super(MainFrame, self).initialise()

        # pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF | pygame.HWACCEL)
        # self.surface = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        self.surface = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF | pygame.HWACCEL)

        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        pygame.display.set_caption("3D Space")
        filename = MainFrame.RESOURCES_DIR + "icon.png"
        alien_file = MainFrame.RESOURCES_DIR + "aliensprite2.png"

        try:
            image = pygame.image.load(filename)
            image = pygame.transform.scale(image, (32, 32))

            image_sheet = spritesheet(alien_file)
            for x in range(0, 9):
                original_image = image_sheet.image_at((x * 39,6,39,27))
                self.alien_images.append((original_image))

            pygame.display.set_icon(image)
        except Exception as err:
            print(str(err))

        self.model = model.World3D(5000, 5000, 10)

        self.model.build(10000)

        # self.model.print()

        self.m2v = ModelToView3D(self.model)

    def draw(self):

        super(MainFrame, self).draw()

        self.surface.fill(Colours.BLACK)
        vx, vy, vz = self.view_pos

        # Get the visible objects from the model
        objs = self.m2v.get_object_list(self.view_pos, self.view_width, self.view_height, self.view_depth)

        # Draw visible objects in reverse order by distance
        distance = sorted(list(objs.keys()), reverse=True)
        for d in distance:
            objs_at_d = objs[d]
            for pos, obj in objs_at_d:
                x, y, z = pos

                size = int(obj.size * self.object_size_scale * (1 - d / self.object_distance_scale))

                # pygame.draw.circle(self.surface,
                #                    MainFrame.COLOURS[obj.type],
                #                    (x, y),
                #                    size)
                #
                # pygame.draw.rect(self.surface, Colours.BLACK,
                #                  (int(x - size / 2), int(y - size / 2), size, size), 0)

                image = pygame.transform.scale(self.alien_images[obj.type], (size, size))
                self.surface.blit(image, (int(x - size / 2), int(y - size / 2), size, size))

        # Draw cross hair
        cross_hair_size = 0.25
        pygame.draw.circle(self.surface, Colours.WHITE, (int(self.view_width / 2), int(self.view_height / 2)), 10, 1)
        pygame.draw.rect(self.surface,
                         Colours.GOLD,
                         (int(self.view_width / 2 * (1 - cross_hair_size)),
                          int(self.view_height / 2 * (1 - cross_hair_size)), int(self.view_width * cross_hair_size),
                          int(self.view_height * cross_hair_size)),
                         2)

        # Draw current view position
        msg = "Pos:{0}".format(self.view_pos)
        text_rect = (0, 0, 100, 30)
        drawText(surface=self.surface,
                 text=msg,
                 color=Colours.GOLD,
                 rect=text_rect,
                 font=pygame.font.SysFont(pygame.font.get_default_font(), 12),
                 bkg=Colours.DARK_GREY)

    def tick(self):

        return

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
    pygame.init()

    view = MainFrame(width=600, height=600)
    view.initialise()

    os.environ["SDL_VIDEO_CENTERED"] = "1"

    FPSCLOCK = pygame.time.Clock()

    pygame.time.set_timer(USEREVENT + 1, 5)
    #pygame.time.set_timer(USEREVENT + 2, 500)
    pygame.event.set_allowed([QUIT, KEYUP, KEYDOWN, USEREVENT])

    loop = True

    while loop is True:

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            view.view_pos = np.add(view.view_pos, np.array(model.World3D.WEST) * 2)
        elif keys[K_RIGHT]:
            view.view_pos = np.add(view.view_pos, np.array(model.World3D.EAST) * 2)

        if keys[K_UP]:
            view.view_pos = np.add(view.view_pos, np.array(model.World3D.DOWN) * 2)
        elif keys[K_DOWN]:
            view.view_pos = np.add(view.view_pos, np.array(model.World3D.UP) * 2)

        if keys[K_q]:
            view.view_pos = np.add(view.view_pos, np.array(model.World3D.NORTH))
        elif keys[K_e]:
            view.view_pos = np.add(view.view_pos, np.array(model.World3D.SOUTH))

        # Loop to process pygame events
        for event in pygame.event.get():

            # Process 1 second timer events
            if event.type == USEREVENT + 1:

                view.tick()

            # Process 0.5 second timer events
            elif event.type == USEREVENT + 2:
                pass

            # Key pressed events
            elif event.type == KEYDOWN:
                pass

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

            if od <= 0 or od > view_depth or abs(ow) > view_width / 2 or abs(oh) > view_height / 2:
                pass
            else:

                # If we don't have a list of objects at this distance then create an empty one
                if od not in objects.keys():
                    objects[od] = []

                # Add ((x,y,z), obj)) to list of objects at this distance
                objects[od].append((
                    (int(ow * (1 - od / self.infinity)) + int(view_width / 2),
                     int(oh * (1 - od / self.infinity)) + int(view_height / 2),
                     od), obj))

        return objects


# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = 2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        textpos = image.get_rect()
        textpos.centerx = rect.centerx
        textpos.y = y

        surface.blit(image, (textpos))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text


if __name__ == "__main__":
    main()
