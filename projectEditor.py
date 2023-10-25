import ctypes
import pygame

class Main:
    def __init__(self):
        self.fps = 60
        self.clock = pygame.time.Clock()

        self.user32 = ctypes.windll.user32
        self.window_size = self.user32.GetSystemMetrics(0), self.user32.GetSystemMetrics(1)
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
