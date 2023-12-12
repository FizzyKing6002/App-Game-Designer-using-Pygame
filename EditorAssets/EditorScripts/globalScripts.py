"""
The file containing global variables and methods, used in object scripts
"""


import os
import shutil


class globalScripts:
    def __init__(self):
        # Globals go here
        self.mouse_pos = [0, 0]
        self.mouse_state = [False, [False, 0], False]

        self.menu_state = 0
        self.change_state = False

        self.dialogue = ["Project Editor opened", "[Project Name] loaded"]

        self.dragging = False
        self.key_dragging = False
        self.dropped = False

        self.generated_obj_num = 0
        self.generator_colour = (0, 0, 0)
        self.generator_pos = [0, 0]
        self.canvas_pos = [0, 0]
        self.canvas_size = [0, 0]

        self.refresh = False
        self.create_new = False

        self.current_path = ""

    # Elapsed time is the time in milliseconds since the last frame
    # Early update is called every frame before any objects are called
    def early_frame_update(self, elapsed_time, mouse_pos, mouse_state, key_state):
        self.mouse_pos = mouse_pos
        self.mouse_state = mouse_state

        if self.refresh:
            self.refresh = False

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
        shutil.copy("EditorAssets/CodeStructs/Commented_Object.py",
                    f"_CurrentProject/{project_name}/Assets/Scripts/ObjectScripts")

        while True:
            try:
                self.current_path = f"_CurrentProject/{project_name}/Assets/Scripts/ObjectScripts/\
Commented_Object{self.generated_obj_num}.py"
                os.rename(f"_CurrentProject/{project_name}/Assets/Scripts/ObjectScripts/\
Commented_Object.py", self.current_path)

            except FileExistsError:
                self.generated_obj_num += 1
                continue
            break

        self.generated_obj_num += 1

        self.change_file_str(self.current_path, "]]",
                             f"0, {self.generator_pos[0]}], [0, {self.generator_pos[1]}",
                                "self.position_modifiers", "[[")
        self.change_file_str(
            self.current_path, "]]", "0, 0.15], [0, 0.15", "self.size_modifiers", "[[")
        self.change_file_str(
            self.current_path, ")", f"{self.generator_colour}"[1:-1], "self.object_colour", "(")

    def change_file_str(self, path, target_until, new_val, *after_strings):
        if os.path.exists(self.current_path):
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
