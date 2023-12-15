"""
The file containing global variables and methods, used in object scripts
"""


import os
import shutil


class globalScripts:
    def __init__(self):
        # Globals go here
        self.project_global_scripts = None

        self.mouse_pos = [0, 0]
        self.mouse_state = [False, [False, 0], False]

        self.menu_state = 0
        self.change_state = False

        self.dialogue = ["Project Editor opened", "[Project Name] loaded"]

        self.dragging = False
        self.key_dragging = False
        self.dropped = False
        self.object_type = None

        self.generated_obj_nums = [0, 0, 0, 0, 0, 0, 0]
        self.generator_colour = (0, 0, 0)
        self.generator_pos = [0, 0]
        self.canvas_pos = [0, 0]
        self.canvas_size = [0, 0]

        self.refresh = False
        self.delayed_refresh = False
        self.create_new = False

        self.current_path = ""

        self.pause_storing_inputs = False

    # Elapsed time is the time in milliseconds since the last frame
    # Early update is called every frame before any objects are called
    def early_frame_update(self, elapsed_time, mouse_pos, mouse_state, key_state):
        self.mouse_pos = mouse_pos
        self.mouse_state = mouse_state

        if self.delayed_refresh:
            self.delayed_refresh = False

        if self.refresh:
            self.refresh = False
            self.delayed_refresh = True

        if self.pause_storing_inputs:
            self.pause_storing_inputs = False

    # Late update is called every frame after all objects have been called
    def late_frame_update(self, elapsed_time, mouse_pos, mouse_state, key_state):
        self.check_dragging_objects()

    def add_dialogue(self, val):
        self.dialogue.pop(0)
        self.dialogue.append(val)

    def customizer_input(self, target_until, new_val, *after_strings):
        self.refresh = True
        self.change_file_str(self.current_path, target_until, new_val, *after_strings)

    def check_dragging_objects(self):
        if self.dropped:
            self.dropped = False

        if self.key_dragging and self.mouse_state[0]:
            self.dragging = True
            self.key_dragging = False

        if self.dragging and not self.mouse_state[0]:
            self.dragging = False
            self.dropped = True

        if self.create_new:
            self.create_new = False

            self.generator_pos[0] = (
                self.generator_pos[0] + self.canvas_size[0] / 2 - self.canvas_pos[0]) \
                    / self.canvas_size[0]
            self.generator_pos[1] = (
                self.generator_pos[1] + self.canvas_size[1] / 2 - self.canvas_pos[1]) \
                    / self.canvas_size[1]

            self.create_object_file()

    def create_object_file(self):
        project_name = os.listdir("_CurrentProject")[0]

        if self.object_type == "duplicate":
            if os.path.exists(self.current_path):
                object_type_file_name = "New_Duplicate"
                index = 6
                self.add_dialogue("Duplicated Object")

                shutil.copy(self.current_path,
                            f"_CurrentProject/{project_name}/Assets/Scripts/ObjectScripts/\
{object_type_file_name}%__create__%.py")

            else:
                return

        else:
            if self.object_type == "image":
                object_type_file_name = "New_Image"
                index = 0
                self.add_dialogue("Created Image Object")

            elif self.object_type == "container":
                object_type_file_name = "New_Container"
                index = 1
                self.add_dialogue("Created Container Object")

            elif self.object_type == "button":
                object_type_file_name = "New_Button"
                index = 2
                self.add_dialogue("Created Button Object")

            elif self.object_type == "text":
                object_type_file_name = "New_Text"
                index = 3
                self.add_dialogue("Created Text Object")

            elif self.object_type == "scroll":
                object_type_file_name = "New_Scroll_Bar"
                index = 4
                self.add_dialogue("Created Scroll Bar")

            elif self.object_type == "text_box":
                object_type_file_name = "New_Text_Box"
                index = 5
                self.add_dialogue("Created Text Box")

            else:
                self.add_dialogue("Object Type Not Found")
                return

            shutil.copy(f"EditorAssets/CodeStructs/{object_type_file_name}.py",
                        f"_CurrentProject/{project_name}/Assets/Scripts/ObjectScripts/\
{object_type_file_name}%__create__%.py")

        while True:
            try:
                self.current_path = f"_CurrentProject/{project_name}/Assets/Scripts/ObjectScripts/\
{object_type_file_name}{self.generated_obj_nums[index]}.py"
                os.rename(f"_CurrentProject/{project_name}/Assets/Scripts/ObjectScripts/\
{object_type_file_name}%__create__%.py", self.current_path)

            except FileExistsError:
                self.generated_obj_nums[index] += 1
                continue
            break

        self.generated_obj_nums[index] += 1

        if self.object_type != "scroll":
            self.change_file_str(self.current_path, "]]",
                                f"0, {self.generator_pos[0]}], [0, {self.generator_pos[1]}",
                                    "self.position_modifiers", "[[")

        if self.object_type != "duplicate":
            self.change_file_str(
                self.current_path, ")", f"{self.generator_colour}"[1:-1], "self.object_colour", "(")

    def change_file_str(self, path, target_until, new_val, *after_strings):
        if os.path.exists(path):
            with open(path, "r") as file:
                file_data = file.read()

            split_data = file_data.split("\n")
            for i, line in enumerate(split_data):
                edited_line = line
                for string in after_strings:
                    if string not in edited_line:
                        break
                    edited_line = edited_line[edited_line.index(string) + len(string):]
                else:
                    new_data = ""
                    start_index = len(line) - len(edited_line)
                    if target_until == "":
                        end_index = len(line)
                    else:
                        end_index = edited_line.index(target_until) + start_index

                    split_data[i] = line[:start_index] + new_val + line[end_index:]

                    for new_line in split_data:
                        new_data += new_line + "\n"
                    if len(new_data) >= 2:
                        new_data = new_data[:-1]

                    with open(f"{path[:-3]}%__cache__%.py", "w") as file:
                        file.write(new_data)

                    with open(path, "w") as file:
                        file.write(new_data)

                    os.remove(f"{path[:-3]}%__cache__%.py")
                    break

    def del_file(self, path):
        if os.path.exists(path):
            os.remove(path)
            self.refresh = True
            self.add_dialogue("Object Deleted")

    def rename_file(self, path, name):
        new_path = ""
        split_path = path.split("/")[:-1] + [f"{name}.py"]
        for directory in split_path:
            new_path += f"{directory}/"
        new_path = new_path[:-1]

        if os.path.exists(new_path):
            self.add_dialogue("File Already Exists")
        else:
            os.rename(path, new_path)
            self.refresh = True
            self.add_dialogue("Object Renamed")
