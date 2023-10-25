import ctypes
import os
import pygame
os.environ["SDL_VIDEO_WINDOW_POS"] = "%d, %d" % (0, 30)

class Main:
    def __init__(self):
        self.fps = 60
        self.clock = pygame.time.Clock()

        user32 = ctypes.windll.user32
        self.window_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1) - 70
        self.window = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
        self.window_object = None

    def main_loop(self):
        run = True

        while run:
            elapsed_time = self.clock.tick(self.fps)

            #update window_object

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEWHEEL:
                    run = False

        pygame.quit()

if __name__ == "__main__":
    main = Main()

    main.main_loop()
