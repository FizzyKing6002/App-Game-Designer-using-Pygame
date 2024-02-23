"""
The file containing global variables and methods, used in object scripts
"""


class globalScripts:
    def __init__(self):
        # Required for scroll bars
        self.mouse_pos = [0, 0]
        # Required for text boxes
        self.mouse_state = [False, [False, 0], False]

        # Globals go here
        self.turn = 0
        self.tiles = []
        self.tile_change = False
        self.move = []
        self.selected_tile = []
        self.black_occ = []
        self.white_occ = []
        self.paused = False
        self.super_tile_change = True
        self.jump_tile = []
        self.delete_jump = -1


    # Elapsed time is the time in milliseconds since the last frame
    # Early update is called every frame before any objects are called
    def early_frame_update(self, elapsed_time, mouse_pos, mouse_state, key_state):
        # Required for scroll bars
        self.mouse_pos = mouse_pos
        # Required for text boxes
        self.mouse_state = mouse_state

    # Late update is called every frame after all objects have been called
    def late_frame_update(self, elapsed_time, mouse_pos, mouse_state, key_state):
        if self.super_tile_change:
            self.tile_change = True
            self.super_tile_change = False

    # Global methods go here
