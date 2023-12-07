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

        self.dragging = False
        self.key_dragging = False
        self.dropped = False

        self.generator_colour = (0, 0, 0)
        self.generator_pos = [0, 0]
        self.generated_obj_num = 0

        self.refresh = False
        self.create_new = False

    # Elapsed time is the time in milliseconds since the last frame
    # Early update is called every frame before any objects are called
    def early_frame_update(self, elapsed_time, mouse_pos, mouse_state, key_state):
        self.mouse_pos = mouse_pos
        self.mouse_state = mouse_state

        if self.refresh:
            self.refresh = False

    # Late update is called every frame after all objects have been called
    def late_frame_update(self, elapsed_time, mouse_pos, mouse_state, key_state):
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

            self.create_object_file()

    def create_object_file(self):
        project_name = os.listdir("_CurrentProject")[0]
        shutil.copy("EditorAssets/CodeStructs/Commented_Object.py",
                    f"_CurrentProject/{project_name}/Assets/Scripts/ObjectScripts")

        while True:
            try:
                path = f"_CurrentProject/{project_name}/Assets/Scripts/ObjectScripts/\
Commented_Object{self.generated_obj_num}.py"
                os.rename(f"_CurrentProject/{project_name}/Assets/Scripts/ObjectScripts/\
Commented_Object.py", path)

            except FileExistsError:
                self.generated_obj_num += 1
                continue
            break

        self.generated_obj_num += 1

#        self.change_file_str(path, "[[0, 0.5], [0, 0.5]]",
 #                               f"[[0, {self.generator_pos[0]}], [0, {self.generator_pos[1]}]]",
  #                              "self.position_modifiers")
        self.change_file_str(path, "[[0, 1], [0, 1]]",
                                "[[0, 0.15], [0, 0.15]]",
                                "self.size_modifiers")
        self.change_file_str(path, "(0, 0, 0)", f"{self.generator_colour}", "self.object_colour")

    def change_file_str(self, path, target, new_val, *required_strings):
        with open(path, "r") as file:
            file_data = file.read()
        
        split_data = file_data.split("\n")
        for i, line in enumerate(split_data):
            for string in required_strings:
                if string not in line:
                    break
            else:
                new_data = ""
                split_data[i] = line.replace(target, new_val)
                for new_line in split_data:
                    new_data += new_line + "\n"
                else:
                    if len(new_data) >= 2:
                        new_data = new_data[:-1]

                with open(f"{path[:-3]}%__cache__%.py", "w") as file:
                    file.write(new_data)
                
                with open(path, "w") as file:
                    file.write(new_data)

                os.remove(f"{path[:-3]}%__cache__%.py")
                break
