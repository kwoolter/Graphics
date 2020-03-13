import pygame
import os
from pygame.locals import *

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
        r,g,b = colour
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        return (r,g,b)


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
    def __init__(self, width: int = 800, height: int = 800):

        super(MainFrame, self).__init__(width, height)

        self.fill_colour = Colours.WHITE

    def initialise(self):

        super(MainFrame, self).initialise()

        self.surface = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF | pygame.HWACCEL)
        # self.surface = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)

        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        pygame.display.set_caption("Colours")
        filename = MainFrame.RESOURCES_DIR + "icon.png"

        try:
            image = pygame.image.load(filename)
            image = pygame.transform.scale(image, (32, 32))
            pygame.display.set_icon(image)
        except Exception as err:
            print(str(err))


    def draw(self):

        self.surface.fill(self.fill_colour)

        pane_rect = self.surface.get_rect()

        x = 0
        y = 0


    def tick(self):

        self.fill_colour = Colours.scale(self.fill_colour, 0.95)

        return

    def update(self):
        pygame.display.update()

    def end(self):
        pygame.quit()


def main():
    pygame.init()

    view = MainFrame()
    view.initialise()

    os.environ["SDL_VIDEO_CENTERED"] = "1"

    FPSCLOCK = pygame.time.Clock()

    pygame.time.set_timer(USEREVENT + 1, 100)
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
            elif event.type == KEYUP:
                pass

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


if __name__ == "__main__":
    main()