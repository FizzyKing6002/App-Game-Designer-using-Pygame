"""
Scroll Bar Object
"""


# Scroll bar needs an image and must be clickable
object_type = {
    "container" : False,
    "text" : False,
    "image" : True,
    "button" : True,
    "hover_activated" : False,
    "key_activated" : False
}
# Name should match container that contains the data that needs to be scrolled
container_name = None

# Class name must be the same as the file name (without .py)
class Commented_Scroll_Bar:
    def __init__(self):
        self.active = False
        # Scroll bar should be drawn over all other images in the container
        self.update_priority = 10000

        self.objects_visible_outside_container = True
        # Image directory for the scroll bar (path from main.py)
        self.img_dir = ""
        self.activation_keys = {}
        # Object is a scroll bar
        self.is_scroll_bar = True

        # [[pixels, percent of container's size], [pixels, percent of container's size]] -> [x, y]
        # Aligns scroll bar to right side of container (for 5% container width scroll bar)
        self.position_modifiers = [[0, 0.975], [0, 0.5]]
        # [[pixels, percent of container's size], [pixels, percent of container's size]] -> [x, y]
        # Sizes scroll bar correctly (scroll bar takes up 5% of the container's width)
        self.size_modifiers = [[0, 0.05], [0, 1]]
        self.rotation_modifiers = [0, 1]
        self.opacity_modifiers = [0, 1]

        self.position_origin = [0.5, 0.5]

        self.text = ""
        self.text_font = ""
        self.text_colour = (0, 0, 0)
        self.text_bold = False
        self.text_italic = False

        # Scroll bar variable definitions
        self.clicked = False
        self.init_mouse_pos = None
        self.mouse_pos_diff = 0
        self.scroll_bar_limit = 0
        self.mouse_scroll_amount = 0
        # Changes how far the scroll bar moves when scrolled -> {float > 0}
        self.scroll_factor = 0.15

    def frame_update(self, global_scripts):
        # While scroll bar is being dragged, it must be moved to the correct position every frame
        self.pos[1] += self.mouse_pos_diff

        # Calculates total movement of scroll bar since it was created
        total_diff = self.mouse_pos_diff + self.position_modifiers[1][0]
        # Total movement of scroll bar including the amount that it would
        # be moved this frame due to scrolling
        total_diff_scroll \
            = total_diff - self.mouse_scroll_amount * self.scroll_factor * self.size[1]

        # If the movement this frame exceeds the maximum allowed position
        if total_diff_scroll > self.scroll_bar_limit:
            # Move the scroll bar to its limit
            self.pos[1] += self.scroll_bar_limit - total_diff
            # Save this change for future frames
            self.position_modifiers[1][0] += self.scroll_bar_limit - total_diff
        # If the movement this frame exceeds the minimum allowed position
        elif total_diff_scroll < 0:
            # Move the scroll bar to its limit
            self.pos[1] -= total_diff
            # Save this change for future frames
            self.position_modifiers[1][0] -= total_diff
        else:
            # Move the scroll bar by the amount scrolled this frame
            self.pos[1] -= self.mouse_scroll_amount * self.scroll_factor * self.size[1]
            # Save this change for future frames
            self.position_modifiers[1][0] \
                -= self.mouse_scroll_amount * self.scroll_factor * self.size[1]

        # If the scroll bar has been let go of this frame
        if not self.clicked and self.init_mouse_pos is not None:
            # Reset variables
            self.init_mouse_pos = None

            # Saved the movement of the scroll bar for future frames
            self.position_modifiers[1][0] += self.mouse_pos_diff
            self.mouse_pos_diff = 0

        # As no method is called when the scroll bar is not clicked,
        # clicked must be set to false every frame
        self.clicked = False

    def left_clicked(self, mouse_pos):
        self.clicked = True
        # If the scroll bar was not being clicked last frame
        if self.init_mouse_pos is None:
            # Set the initial mouse position that the scroll bar was clicked on at
            self.init_mouse_pos = mouse_pos[1]
        # Find the distance that the mouse has moved since the scroll bar was clicked (y axis)
        self.mouse_pos_diff = mouse_pos[1] - self.init_mouse_pos

        # Calculates total movement of scroll bar since it was created
        total_diff = self.mouse_pos_diff + self.position_modifiers[1][0]

        # If the total movement exceeds the maximum allowed position
        if total_diff > self.scroll_bar_limit:
            # Move scroll bar to maximum allowed position
            self.mouse_pos_diff = self.scroll_bar_limit - self.position_modifiers[1][0]
        # If the total movement exceeds the minimum allowed position
        elif total_diff < 0:
            # Move scroll bar to minimum allowed position
            self.mouse_pos_diff = 0 - self.position_modifiers[1][0]

    def middle_clicked(self, mouse_pos):
        pass

    def right_clicked(self, mouse_pos):
        pass

    def hovered_over(self, mouse_pos):
        pass

    def key_input(self, key):
        pass
