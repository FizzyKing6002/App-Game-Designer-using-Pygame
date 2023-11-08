"""
The main file of the project.

Imports:
    ctypes:
        Gets the size of the screen
    os:
        Lists file directories and controls default window position
    pygame:
        Creates the clock and window, gets window events,
        updates the window display and closes the window
    ImportCode.objects:
        Creates objects that interact with the user and window
    EditorScripts.ObjectScripts:
        Package that imports saved objects
    EditorScripts.GlobalScripts:
        Class is passed to objects where it is used as global variables and methods

Classes:
    Main
"""

import ctypes
import os
import pygame
from ImportCode import objects
# Import the package so that files within the folder can be accessed through the package
from EditorScripts import ObjectScripts
from EditorScripts import globalScripts

# Initialises pygame, including pygame.font, allowing certain pygame methods to be used
pygame.init()
# Initialises the position of a generated window
os.environ["SDL_VIDEO_WINDOW_POS"] = "0, 30"

class Main:
    """
    Controls the flow of the program including updating graphics,
    loading objects and calling objects every frame.

    Attributes:
        fps:
            Ideal fps of the program
        clock:
            Limits fps of program to self.fps
        window:
            Creates a resizable window
        objects:
            Contains all the objects in the program (most within other objects)
        global_scripts:
            Instance of class that contains 'global' methods and attributes.

    Methods:
        __call__():
            Startup method calls load_objects and main_loop
        load_objects():
            Locates the object files and orders them based on which containers they belong to
            Calls recursive_create_objects after object ordering
        recursive_create_objects(objects_list, val, path):
            Searches through the objects_list for objects that belong to the container named 'val',
            appends these objects the list located within that container given by 'path'
            Calls itself for every object it appended that is also a container,
            changing 'val' to the name of this container and adding the object to the 'path'
        call_objects(elapsed_time):
            Calls every object contained within the 'objects' attribute
            Passes information about the window, time, user input, and global_scripts
        main_loop():
            Calls call_objects, handles window events, and updates the window every frame 
    """

    def __init__(self):
        self.fps = 120
        self.clock = pygame.time.Clock()

        user32 = ctypes.windll.user32
        # Window height is reduced by 70 pixels to account for the taskbar and title bar
        window_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1) - 70
        self.window = pygame.display.set_mode(window_size, pygame.RESIZABLE)
        self.objects = []

        # Creates an instance of the class located within globalScripts.py
        self.global_scripts = globalScripts.globalScripts()

    def __call__(self):
        # Objects are loaded before the program loop begins
        self.load_objects()
        self.main_loop()

    def load_objects(self):
        # Creates a list of lists, where each list's first item is the container name and
        # the rest of the items are object's file names that belong to the specified container
        objects_list = []
        # List is created of all the file names within the ObjectScripts folder
        object_files = os.listdir("EditorScripts/ObjectScripts")

        for file_name in object_files:
            # The __init__.py file and non python files cannot be loaded, so are ignored
            if file_name == "__init__.py" or file_name[-3:] != ".py":
                continue

            # Gets the container name attribute from the current file
            exec(f"container_name = ObjectScripts.{file_name[:-3]}.container_name",
                 locals(), globals())

            # Base case - new list should be created if none already exist
            if len(objects_list) == 0:
                objects_list.append([container_name, file_name[:-3]])
                continue
            # Searches through existing lists for matching container names
            for container_type in objects_list:
                # When matching container name is found, adds current file name to the list
                if container_name == container_type[0]:
                    container_type.append(file_name[:-3])
                    break

                # If matching container name is not found, creates a new list
                if container_type == objects_list[-1]:
                    objects_list.append([container_name, file_name[:-3]])
                    break

        # Calls method to create objects using the ordered list just created
        self.recursive_create_objects(objects_list, None, "self.objects")

    def recursive_create_objects(self, objects_list, val, path):
        # Gets all of the lists of objects belonging to containers
        for container_type in objects_list:
            # If the container for the objects matches the target container name
            if container_type[0] == val:
                # Gets the objects that should belong to this container
                for i, object_name in enumerate(container_type):
                    # Ignore the container name as it is not an object
                    if i == 0:
                        continue

                    # Get the object types and class of the object from the object's file
                    exec(f"object_type = ObjectScripts.{object_name}.object_type",
                         locals(), globals())
                    exec(f"object_class = ObjectScripts.{object_name}.{object_name}",
                         locals(), globals())
                    # Creates the object inside the correct container given by the path
                    exec(f"""{path}.append(objects.Object(object_type['container'],
                                                          object_type['text'],
                                                          object_type['image'],
                                                          object_type['button'],
                                                          object_type['hover_activated'],
                                                          object_type['key_activated'],
                                                          object_class
                                                          ))""", locals(), globals())

                    # If the object is a container
                    if object_type['container']:
                        # Search for and add objects to it that should belong to it
                        self.recursive_create_objects(
                            objects_list, object_name, f"{path}[{i-1}].objects")
                break

    def call_objects(self, elapsed_time):
        for obj in self.objects:
            # Calls the object's __call__ method
            obj(self.window, elapsed_time,
                # Center coordinates of window is (half its width, half its height)
                [self.window.get_width() / 2, self.window.get_height() / 2],
                [self.window.get_width(), self.window.get_height()],
                # Rotation of window is zero, opacity is one
                0, 1,
                pygame.mouse.get_pos(), pygame.mouse.get_pressed(),
                pygame.key.get_pressed(),
                self.global_scripts)

    def main_loop(self):
        # Objects are called once before the program begins so that everything is initialised
        self.call_objects(0)

        run = True
        elapsed_time = 0

        while run:
            # Update every object
            self.call_objects(elapsed_time)

            for event in pygame.event.get():
                # If the close button in the title bar is clicked
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEWHEEL:
                    run = False

            pygame.display.update()

            # Get the amount of time that has passed during this frame,
            # waiting until the fps required time is reached if required
            elapsed_time = self.clock.tick(self.fps)

        # Close the window after the program loop is exited
        pygame.quit()


# If this file was run without being imported
if __name__ == "__main__":
    # Create an instance of the Main class
    main = Main()
    # Call the __call__ function of the object
    main()
