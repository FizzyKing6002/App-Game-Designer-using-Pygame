import ctypes
import os
import pygame
from ImportCode import objects
from EditorScripts import ObjectScripts

os.environ["SDL_VIDEO_WINDOW_POS"] = "%d, %d" % (0, 30)

class Main:
    def __init__(self):
        self.fps = 60
        self.clock = pygame.time.Clock()

        user32 = ctypes.windll.user32
        self.window_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1) - 70
        self.window = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
        self.objects = []

    def __call__(self):
        self.load_objects()
        self.main_loop()

    def load_objects(self):
        objects_list = []
        object_files = os.listdir("EditorScripts/ObjectScripts")
        for file_name in object_files:
            if file_name == "__init__.py" or file_name[-3:] != ".py":
                continue

            exec(f"container_name = ObjectScripts.{file_name[:-3]}.container_name",
                 locals(), globals())

            if len(objects_list) == 0:
                objects_list.append([container_name, file_name[:-3]])
                continue

            for container_type in objects_list:
                if container_name == container_type[0]:
                    container_type.append(file_name[:-3])
                    break

                if container_type == objects_list[-1]:
                    objects_list.append([container_name, file_name[:-3]])
                    break

        self.recursive_create_objects(objects_list, None, "self.objects")

    def recursive_create_objects(self, objects_list, val, path):
        for container_type in objects_list:
            if container_type[0] == val:
                for i, object_name in enumerate(container_type):
                    if i == 0:
                        continue

                    exec(f"object_type = ObjectScripts.{object_name}.object_type",
                         locals(), globals())
                    exec(f"object_class = ObjectScripts.{object_name}.{object_name}",
                         locals(), globals())
                    exec(f"""{path}.append(objects.Object(object_type['container'],
                                                          object_type['image'],
                                                          object_type['button'],
                                                          object_type['hover_activated'],
                                                          object_type['key_activated'],
                                                          object_class
                                                          ))""", locals(), globals())

                    if object_type['container']:
                        self.recursive_create_objects(
                            objects_list, object_name, f"{path}[{i-1}].objects")

                break

    def call_objects(self, elapsed_time):
        for obj in self.objects:
            obj(self.window, elapsed_time,
                [self.window_size[0], self.window_size[1]],
                self.window_size, 0, 1,
                pygame.mouse.get_pos(), pygame.mouse.get_pressed(),
                pygame.key.get_pressed())

    def main_loop(self):
        run = True
        while run:
            elapsed_time = self.clock.tick(self.fps)

            self.call_objects(elapsed_time)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEWHEEL:
                    run = False

        pygame.quit()

if __name__ == "__main__":
    main = Main()

    main()
