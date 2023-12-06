"""
The file containing global variables and methods, used in object scripts
"""


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

    # Elapsed time is the time in milliseconds since the last frame
    # Early update is called every frame before any objects are called
    def early_frame_update(self, elapsed_time, mouse_pos, mouse_state, key_state):
        self.mouse_pos = mouse_pos
        self.mouse_state = mouse_state

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
