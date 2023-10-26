import ctypes
import os
import pygame
from ImportCode import objects

os.environ["SDL_VIDEO_WINDOW_POS"] = "%d, %d" % (0, 30)

class Main:
    def __init__(self):
        self.fps = 60
        self.clock = pygame.time.Clock()

        user32 = ctypes.windll.user32
        self.window_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1) - 70
        self.window = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
        self.window_object = objects.Object(True, False, False, False, False, None)

    def main_loop(self):
        run = True

        while run:
            elapsed_time = self.clock.tick(self.fps)

            self.window_object(self.window, elapsed_time,
                               [self.window_size[0], self.window_size[1]],
                               self.window_size, 0, 1,
                               pygame.mouse.get_pos(), pygame.mouse.get_pressed(),
                               pygame.key.get_pressed())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEWHEEL:
                    run = False

        pygame.quit()

if __name__ == "__main__":
    main = Main()

    main.main_loop()
