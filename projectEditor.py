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
import importlib
import shutil

import pygame

from EditorAssets.ImportCode import objects
# Imports the package so that files within the folder can be accessed through the package
from EditorAssets.EditorScripts import globalScripts

# Initialises pygame, including pygame.font, allowing certain pygame methods to be used
pygame.init()

user32 = ctypes.windll.user32
# Window height is reduced by 70 pixels to account for the taskbar and title bar
window_size = int(user32.GetSystemMetrics(0) / 1.5), int((user32.GetSystemMetrics(1) - 70) / 1.5)
# Initialises the position of a generated window
os.environ["SDL_VIDEO_WINDOW_POS"] = f"{window_size[0] / 2}, {(30 + window_size[0]) / 2}"


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
        import_objects(path, object_files):
            Imports all objects from Object Scripts into a list
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
        window_title = "Project Editor"
        window_icon_path = "EditorAssets/Textures/maintenance.png"

        # Change the title of the window
        pygame.display.set_caption(window_title)
        # Change the icon of the window
        if os.path.exists(window_icon_path):
            pygame.display.set_icon(pygame.image.load(window_icon_path))
        # Change the icon in the taskbar
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(window_icon_path)

        self.fps = 120
        self.clock = pygame.time.Clock()

        self.window = pygame.display.set_mode(window_size, pygame.RESIZABLE)

        self.objects = []

        # Creates an instance of the class located within globalScripts.py
        self.editor_global_scripts = globalScripts.globalScripts()

        # Ensures the directories exist before importing user objects
        if not os.path.isdir("_CurrentProject"):
            os.mkdir("_CurrentProject")
        current_projects = os.listdir("_CurrentProject")
        if len(current_projects) == 0:
            shutil.copytree("EditorAssets/CodeStructs/NewProject", "_CurrentProject/NewProject")
            project_name = "NewProject"
        else:
            project_name = current_projects[0]
        if not os.path.isdir(f"_CurrentProject/{project_name}/Assets/Scripts/ObjectScripts"):
            os.mkdir(f"_CurrentProject/{project_name}/Assets/Scripts/ObjectScripts")
        # Creates an instance of the class located within the user's globalScripts.py
        global_scripts = importlib.import_module(
            f"_CurrentProject.{project_name}.Assets.Scripts.globalScripts")
        self.editor_global_scripts.project_global_scripts = global_scripts.globalScripts()
        self.editor_global_scripts.project_global_scripts.__editor_attr__current_path__ = ""

        # Ensures project object modules are saved so they can be reloaded later
        self.project_obj_files = []

    def __call__(self):
        # Objects are loaded before the program loop begins
        self.load_editor_objects()
        self.main_loop()

    def load_editor_objects(self):
        # Creates a list of lists, where each list's first item is the container name and
        # the rest of the items are object's file names that belong to the specified container
        objects_list = []

        # Imports all the objects from the object scripts folders and composes a list of these files
        # Passes path from this file to the folders
        editor_obj_files, _ = self.import_objects(
            "EditorAssets/EditorScripts/ObjectScripts/", [], [])

        # Allows the object files to be accessible from other files
        self.editor_global_scripts.object_files = editor_obj_files

        for file in editor_obj_files:
            # Gets the container name attribute from the current file
            container_names = file.container_name

            # Turns container_names into a list iterable
            if not isinstance(container_names, list):
                container_names = [container_names]

            for container_name in container_names:
                self.fill_container_list(objects_list, file, container_name)

        # Calls method to create objects using the ordered list just created
        self.recursive_create_objects(objects_list, None, "self.objects")

    def load_project_objects(self):
        # Creates a list of lists, where each list's first item is the container name and
        # the rest of the items are object's file names that belong to the specified container
        objects_list = []

        # Ensures the directories exist before importing user objects
        if not os.path.isdir("_CurrentProject"):
            os.mkdir("_CurrentProject")
        current_projects = os.listdir("_CurrentProject")
        if len(current_projects) == 0:
            shutil.copytree("EditorAssets/CodeStructs/NewProject", "_CurrentProject/NewProject")
            project_name = "NewProject"
        else:
            project_name = current_projects[0]
        if not os.path.isdir(f"_CurrentProject/{project_name}/Assets/Scripts/ObjectScripts"):
            os.mkdir(f"_CurrentProject/{project_name}/Assets/Scripts/ObjectScripts")

        # Reloads global scripts as they may have been altered
        global_scripts = importlib.reload(importlib.import_module(
            f"_CurrentProject.{project_name}.Assets.Scripts.globalScripts"))
        self.editor_global_scripts.project_global_scripts = global_scripts.globalScripts()
        self.editor_global_scripts.project_global_scripts.__editor_attr__current_path__ \
            = self.editor_global_scripts.current_path

        # Create a pointer list to show whether modules are still being used
        pointer_list = []
        for _ in self.project_obj_files:
            pointer_list.append(False)

        # Invalidates cached imports so that when modules are reloaded
        # they are done so with the updated file
        importlib.invalidate_caches()
        # Imports all the objects from the object scripts folders and extends a list of these files
        # Passes path from this file to the folders
        object_files, pointer_list = self.import_objects(
            f"_CurrentProject/{project_name}/Assets/Scripts/ObjectScripts/", [], pointer_list)
        self.project_obj_files += object_files

        # All the unused modules are removed from the project object files list
        len_pointer_list = len(pointer_list)
        for i, boolean in enumerate(pointer_list):
            if not boolean:
                self.project_obj_files.pop(i - len_pointer_list)

        for file in self.project_obj_files:
            # Gets the container name attribute from the current file
            container_names = file.container_name

            # Turns container_names into a list iterable
            if not isinstance(container_names, list):
                container_names = [container_names]

            for container_name in container_names:
                self.fill_container_list(objects_list, file, container_name)

        # Makes container structure accessible to list window in interface
        self.editor_global_scripts.container_list = objects_list

        # Calls method to create objects using the ordered list just created
        # self.objects[0] goes into the background object
        # .objects[0] goes into the canvas object (AS OBJECTS HAVE NOT BEEN SORTED YET)
        self.recursive_create_objects(objects_list, None,
                                      "self.objects[0].objects[-2].objects[0].objects")

    def import_objects(self, path, object_files, pointer_list):
        # Iterates through every file in the folder
        for file in os.listdir(f"{os.path.dirname(__file__)}/{path}"):
            # Ignore non object scripts
            if file == "__init__.py" or file[-3:] != ".py":
                # If the non object script is a folder import the objects in that folder
                if os.path.isdir(f"{os.path.dirname(__file__)}/{path}{file}"):
                    self.import_objects(f"{path}{file}/", object_files, pointer_list)
                continue

            # importlib.import_module returns the imported module
            module = importlib.import_module(f"{path.replace('/', '.')}{file[:-3]}")

            # If the module has been imported before
            if module in self.project_obj_files:
                # Reload the module so that changes are up to date
                importlib.reload(module)
                # Update the pointer list to show that the module is still being used
                index = self.project_obj_files.index(module)
                pointer_list[index] = True
            else:
                object_files.append(module)
                pointer_list.append(True)
            del file

        return object_files, pointer_list

    def fill_container_list(self, objects_list, file, container_name):
        # Base case - new list should be created if none already exist
        if len(objects_list) == 0:
            objects_list.append([container_name, file])
            return
        # Searches through existing lists for matching container names
        for container_type in objects_list:
            # When matching container name is found, adds current file name to the list
            if container_name == container_type[0]:
                container_type.append(file)
                break

            # If matching container name is not found, creates a new list
            if container_type == objects_list[-1]:
                objects_list.append([container_name, file])
                break

    def recursive_create_objects(self, file_list, target_container, path):
        # Iterates through lists of files belonging to different containers
        for container_type in file_list:
            # If the container for the objects matches the target container name
            if container_type[0] == target_container:
                # Gets the objects that should belong to this container
                for i, file in enumerate(container_type):
                    # Ignore the container name as it is not an object
                    if i == 0:
                        continue

                    # Get the object types, file name, and main class of the file
                    object_type = file.object_type
                    file_name = file.__name__.split(".")[-1]
                    object_class = file.Main

                    # Creates the object inside the correct container given by the path
                    if path[:46] == "self.objects[0].objects[-2].objects[0].objects":
                        exec(f"""{path}.append(objects.Object(object_type['container'],
                                                            object_type['text'],
                                                            object_type['image'],
                                                            object_type['button'],
                                                            object_type['hover_activated'],
                                                            object_type['key_activated'],
                                                            object_class, file_name
                                                            ))""", locals(), globals())
                    else:
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
                            file_list, file_name, f"{path}[{i-1}].objects")

                # If the correct list is found, the others do not need to be checked
                break

    def call_objects(self, elapsed_time, mouse_wheel_movement, text_input):
        # Center coordinates of window is (half its width, half its height)
        window_pos = [self.window.get_width() / 2, self.window.get_height() / 2]
        window_size = [self.window.get_width(), self.window.get_height()]

        mouse_pos = pygame.mouse.get_pos()
        mouse_state = list(pygame.mouse.get_pressed())
        key_state = pygame.key.get_pressed()

        # Add mouse wheel movement to the middle click in mouse state
        mouse_state[1] = [mouse_state[1], mouse_wheel_movement]

        # Calls global update function before objects
        self.editor_global_scripts.early_frame_update(
            elapsed_time, mouse_pos, mouse_state, key_state)

        for obj in self.objects:
            # Calls the object's __call__ method
            obj(self.window, elapsed_time, window_pos, window_size,
                # Rotation of window is zero, opacity is one
                0, 1,
                mouse_pos, mouse_state, key_state, text_input,
                # The objects should not be lame by default
                False, False,
                self.editor_global_scripts)

        # Calls global update function after objects
        self.editor_global_scripts.late_frame_update(
            elapsed_time, mouse_pos, mouse_state, key_state)

    def main_loop(self):
        # Objects are called once before the program begins so that everything is initialised
        # Elapsed time is zero so that animations are not progressed,
        # mouse scroll is defaulted to zero
        self.call_objects(0, 0, "")

        # Project objects are loaded after the editor objects have been ordered correctly
        self.load_project_objects()

        run = True
        elapsed_time = 0

        while run:
            # Mouse wheel movement set to zero each frame as previous movement would persist
            mouse_wheel_movement = 0
            # Likewise for text input
            text_input = ""

            for event in pygame.event.get():
                # If the close button in the title bar is clicked
                if event.type == pygame.QUIT:
                    run = False

                # Mouse wheel movement must be fetched from the event handler
                if event.type == pygame.MOUSEWHEEL:
                    # Mouse wheel movement is fetched, mouse wheel only moves in y direction
                    mouse_wheel_movement = event.y

                # Getting unicode text input is done through the event handler
                # to avoid unnecessary processing
                if event.type == pygame.KEYDOWN:
                    if event.key not in (pygame.K_BACKSPACE, pygame.K_RETURN):
                        # Turns the text related event into unicode
                        text_input = event.unicode

            if self.editor_global_scripts.refresh:
                # Refreshing objects involved reloading all project objects
                self.load_project_objects()

            # Update every object
            self.call_objects(elapsed_time, mouse_wheel_movement, text_input)

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
