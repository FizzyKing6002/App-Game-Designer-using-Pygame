"""
The file containing global variables and methods, used in object scripts
"""


class globalScripts:
    def __init__(self):
        # Globals go here
        self.menu_state = 0

    # Elapsed time is the time in milliseconds since the last frame
    # Early update is called every frame before any objects are called
    def early_frame_update(self, elapsed_time, mouse_pos, mouse_state, key_state):
        pass

    # Late update is called every frame after all objects have been called
    def late_frame_update(self, elapsed_time, mouse_pos, mouse_state, key_state):
        pass
