"""
Framework file for window objects

Imports:
    copy:
        Allows lists to be copied without mutability
    pygame:
        Vector math, loading images, transforming images, drawing images, creating surfaces
    ImportCode.animation:
        Handles animations

Methods:
    Object(*args):
        Defines variables to be used in class inheritance, returns instance of Object class

Classes:
    Object(Container, Text, Image, Button, Hover_Activated, Key_Activated, object_class):
        Inherits classes based upon the type of object that is being created,
        always inherits object_class
        Contains default object requirements such as position and size
        Calculates default object requirements and calls animations
        Handles the update from the main program every frame
    Container():
        For objects of type container
        Handles updating containers' objects
    Text():
        For objects of type text
        Handles creating fonts and text
    Image():
        For objects of type image
        Handles drawing images to the screen
    Button():
        For objects of type button
        Calls relevant method when object is clicked
    Hover_Activated():
        For objects of type hover_activated
        Calls relevant method when object is hovered over
    Key_Activated():
        For objects of type key_activated
        Calls relevant method when key is clicked that the object reacts to
    None1():
        Empty class is inherited when object is not of type container
    None2():
        Empty class is inherited when object is not of type text
    None3():
        Empty class is inherited when object is not of type image
    None4():
        Empty class is inherited when object is not of type button
    None5():
        Empty class is inherited when object is not of type hover_activated
    None6():
        Empty class is inherited when object is not of type key_activated
"""


import copy
import pygame
# Import is relative to the Project Editor file
from EditorAssets.ImportCode import animation


# Factory function is used that returns a class object,
# neccessary as variables must be defined before class is initialised
def Object(*args):
    container, text, image, button, hover_activated, key_activated, object_class = args

    class Object(Container if container else None1,
                 Text if text else None2,
                 Image if image else None3,
                 Button if button else None4,
                 Hover_Activated if hover_activated else None5,
                 Key_Activated if key_activated else None6,
                 object_class):
        """
        Attributes:
            pos:
                Current position of the center of the object -> x, y
            size:
                Current dimensions of the object -> x, y
            rot:
                Current rotation of the object
            opa:
                Current opacity of the object
            animations:
                Stores all animations of the object

        Methods:
            __call__(window, time,
                     con_pos, con_size, con_rot, con_opa,
                     mouse_pos, mouse_state, key_state, global_scripts):
                Called every frame when the object is updated
                Responsible for calling all of the objects methods
            animate(time):
                Updates every animation that the object has using the Animation file
            create_animation(val, time, anim_type, *args):
                Appends animation to the object's animation list using Animation file
            calc_attr(con_pos, con_size, con_rot, con_opa):
                Calculates object's attributes based upon the attribute modifiers
                (found in the object's object class) and the object's container's attributes
            calc_mouse_pos(mouse_pos):
                Returns new mouse position relative to the rotation of the object
        """

        def __init__(self):
            self.pos = [0, 0]
            self.size = [0, 0]
            self.rot = 0
            self.opa = 1

            self.animations = []

            if container:
                # Initialises container class as the __init__ is overwritten
                Container.__init__(self)

            # Initialises object class as the __init__ is overwritten
            object_class.__init__(self)

            if image:
                # Initialises image class as the __init__ is overwritten
                Image.__init__(self)

        def __call__(self, window, time,
                     con_pos, con_size, con_rot, con_opa, mouse_pos, mouse_state, key_state,
                     text_input, is_lame, is_storing_inputs, global_scripts):
            # If the object is not currently active
            if not self.active:
                # Call the frame update method so that it is able to become active again if needed
                self.frame_update(global_scripts)
                return

            self.animate(time)
            self.calc_attr(con_pos, con_size, con_rot, con_opa)
            # Redefine position of mouse before checking hitbox collisions or calling child objects
            mouse_pos = self.calc_mouse_pos(mouse_pos)

            # hasattr() checks whether the attribute exists,
            # callable() checks whether the attribute is a method or not

            # If the object is lame, only call the methods that are necessary
            if is_lame:
                if hasattr(self, "draw_image") and callable(self.draw_image):
                    self.draw_image(window)
                if hasattr(self, "draw_text") and callable(self.draw_text):
                    self.draw_text(window)

                if hasattr(self, "container_update") and callable(self.container_update):
                    self.container_update(window, time, mouse_pos, mouse_state,
                                          key_state, text_input, True, False, global_scripts)
                return
            # If this object makes contained objects lame
            if hasattr(self, "objects_are_lame") and self.objects_are_lame:
                is_lame = True

            if is_storing_inputs:
                if hasattr(self, "call_clicked") and callable(self.call_clicked):
                    self.call_clicked(mouse_pos, mouse_state)
                elif hasattr(self, "call_hovered") and callable(self.call_hovered):
                    self.call_hovered(mouse_pos)
                if hasattr(self, "call_activated") and callable(self.call_activated):
                    self.call_activated(key_state, text_input)

                if hasattr(self, "draw_image") and callable(self.draw_image):
                    self.draw_image(window)
                if hasattr(self, "draw_text") and callable(self.draw_text):
                    self.draw_text(window)

                if hasattr(self, "container_update") and callable(self.container_update):
                    self.container_update(window, time, mouse_pos, mouse_state,
                                          key_state, text_input, is_lame, True, global_scripts)
                return
            # If this object makes contained objects store inputs
            if hasattr(self, "objects_are_storing_inputs") and self.objects_are_storing_inputs:
                is_storing_inputs = True

            if hasattr(self, "call_clicked") and callable(self.call_clicked):
                self.call_clicked(mouse_pos, mouse_state)
            elif hasattr(self, "call_hovered") and callable(self.call_hovered):
                self.call_hovered(mouse_pos)

            if hasattr(self, "call_activated") and callable(self.call_activated):
                self.call_activated(key_state, text_input)

            self.frame_update(global_scripts)

            if hasattr(self, "draw_image") and callable(self.draw_image):
                self.draw_image(window)
            if hasattr(self, "draw_text") and callable(self.draw_text):
                self.draw_text(window)

            if hasattr(self, "container_update") and callable(self.container_update):
                self.container_update(window, time, mouse_pos, mouse_state, key_state, text_input,
                                      is_lame, is_storing_inputs, global_scripts)

        def animate(self, time):
            for anim in self.animations:
                # If the animation already completed
                if (anim[0] == 2 and not anim[8]) or (anim[0] == 0 and anim[8]):
                    continue

                # Update animation
                anim = animation.animate(anim, time)

        def create_animation(self, val, time, anim_type, *args):
            # Create animation from animation file
            self.animations.append(animation.create_animation(val, time, anim_type, *args))

        def get_complete_animation(self, name):
            for anim in self.animations:
                # If the target animation is found
                if anim[7] == name:
                    # Return if the animation is complete or not
                    if anim[0] == 1:
                        return False
                    return True

        def complete_animation(self, name):
            for anim in self.animations:
                # If the target animation is found
                if anim[7] == name:
                    # Complete the animation
                    if anim[8]:
                        anim[3] = 0
                        anim[0] = 0
                    else:
                        anim[3] = anim[4]
                        anim[0] = 2

        def delete_animation(self, name):
            temp_anim_list = copy.deepcopy(self.animations)

            for anim in temp_anim_list:
                # If the target animation is found
                if anim[7] == name:
                    # Delete the animation
                    self.animations.remove(anim)

        def progress_animation(self, name, time):
            for anim in self.animations:
                # If the target animation is found
                if anim[7] == name:
                    # Complete the animation
                    if anim[8]:
                        anim[3] -= time
                    else:
                        anim[3] += time

        def reverse_animation(self, name, *args):
            for anim in self.animations:
                # If the target animation is found
                if anim[7] == name:
                    # Reverse the animation
                    if len(args) == 0:
                        anim[0] = 1
                        anim[8] = not anim[8]
                    else:
                        if anim[8] != args[0]:
                            anim[0] = 1

                        anim[8] = args[0]

        def calc_attr(self, con_pos, con_size, con_rot, con_opa):
            pos_mod = copy.deepcopy(self.position_modifiers)
            size_mod = copy.deepcopy(self.size_modifiers)
            rot_mod = copy.deepcopy(self.rotation_modifiers)
            opa_mod = copy.deepcopy(self.opacity_modifiers)

            # Add values from object's animations to attributes
            for anim in self.animations:
                j = 0
                if "%" in anim[5]:
                    j = 1

                if "x" in anim[5] and "y" not in anim[5]:
                    i = 0
                elif "y" in anim[5] and "x" not in anim[5] and "opa" not in anim[5]:
                    i = 1
                else:
                    if "pos" in anim[5]:
                        pos_mod[0][j] += anim[1][0]
                        pos_mod[1][j] += anim[1][1]
                    elif "size" in anim[5]:
                        size_mod[0][j] += anim[1][0]
                        size_mod[1][j] += anim[1][1]
                    elif "rot" in anim[5]:
                        rot_mod[j] += anim[1]
                    elif "opa" in anim[5]:
                        opa_mod[j] += anim[1]
                    continue

                if "pos" in anim[5]:
                    pos_mod[i][j] += anim[1]
                elif "size" in anim[5]:
                    size_mod[i][j] += anim[1]

            self.pos = [
                con_pos[0] + con_size[0] * (pos_mod[0][1] - 0.5) + pos_mod[0][0],
                con_pos[1] + con_size[1] * (pos_mod[1][1] - 0.5) + pos_mod[1][0]
            ]
            self.size = [
                # Size cannot be negative
                max(con_size[0] * size_mod[0][1] + size_mod[0][0], 0),
                max(con_size[1] * size_mod[1][1] + size_mod[1][0], 0)
            ]
            self.rot = con_rot * rot_mod[1] + rot_mod[0]
            # Opacity is a percentage therefore must be between 0 and 1
            self.opa = min(max(con_opa * opa_mod[1] + opa_mod[0], 0), 1)

            # Change the position of the object depending on
            # which part of the object the user wants the position to refer to
            self.pos[0] -= (self.position_origin[0] - 0.5) * self.size[0]
            self.pos[1] -= (self.position_origin[1] - 0.5) * self.size[1]

            # Resizes the object based upon its limits of ratio of x and y
            if hasattr(self, "min_max_size"):
                if self.min_max_size[0][0] is not None:
                    self.size[0] = max(self.size[0], self.min_max_size[0][0] * self.size[1])
                if self.min_max_size[1][0] is not None:
                    self.size[1] = max(self.size[1], self.min_max_size[1][0] * self.size[0])
                if self.min_max_size[0][1] is not None:
                    self.size[0] = min(self.size[0], self.min_max_size[0][1] * self.size[1])
                if self.min_max_size[1][1] is not None:
                    self.size[1] = min(self.size[1], self.min_max_size[1][1] * self.size[0])

        def calc_mouse_pos(self, mouse_pos):
            # Mouse position does not need to be recalculated if the object is not rotated
            if self.rot != 0:
                # Create vector of mouse position from center of object
                # Rotate vector by the rotation of the object
                vector = pygame.math.Vector2(mouse_pos[0] - self.pos[0],
                                             mouse_pos[1] - self.pos[1]).rotate(self.rot)
                # Add the vector to the center of the object coordinates
                mouse_pos = [
                    self.pos[0] + vector[0],
                    self.pos[1] + vector[1]
                ]

            return mouse_pos

    # Returns instance of Object class
    return Object()

class Container:
    """
    Attributes:
        objects:
            List of objects belonging to the container
        object_offset:
            Used for scroll bar functionality
            If objects extend negatively beyond the boundary of the container,
            this offset repositions them to within the boundary
        prev_scroll_offset:
            Used for scroll bar functionality
            Gets the offset for all objects to be moved from the last frame due to the scroll bar,
            which is used in the current frame's calculations

    Methods:
        container_update(window, time, mouse_pos, mouse_state, key_state, global_scripts):
            Performs logic for how the objects of the container should be updated
        call_objects(surface, time, mouse_pos, mouse_state, key_state,
                     global_scripts, container_has_scroll_bar, scroll_offset):
            Calls all of container's objects, passing its attributes to them
        calc_size_scroll_bar():
            Works out the ratio of the difference between maximum and minimum position
            of objects within the container to the size of the container
            Returns size that the scroll bar should be,
            object offset due to objects ouside of container limits
    """

    def __init__(self):
        self.objects = []
        # Offset due to objects poking out of the top of the container
        self.object_offset = 0
        self.prev_scroll_offset = 0

    def container_update(self, window, time, mouse_pos, mouse_state,
                         key_state, text_input, is_lame, is_storing_inputs, global_scripts):
        # In the canvas user objects are stored therefore the project global scripts should be used
        if hasattr(self, "__is_editor_canvas__") and self.__is_editor_canvas__:
            global_scripts = global_scripts.project_global_scripts

        # Objects are sorted by their update_priority attribute
        self.objects.sort(key=lambda x: x.update_priority, reverse=False)

        container_has_scroll_bar = False
        scroll_offset = 0
        # Search for a scroll bar within objects
        for obj in self.objects:
            if obj.is_scroll_bar:
                container_has_scroll_bar = True

                # Avoid division by zero error
                if obj.size[1] != 0 and self.size[1] - obj.size[1] != 0:
                    # Calculate how far to scroll objects upwards
                    # based upon scroll bar progress through the container
                    scroll_offset = ((self.size[1] ** 2) / obj.size[1] - self.size[1]) \
                        * ((obj.position_modifiers[1][0] + obj.mouse_pos_diff) \
                            / (self.size[1] - obj.size[1]))

                    # Amount scroll wheel has been moved since last frame
                    obj.mouse_scroll_amount = 0
                    if hitbox_collision(self, mouse_pos):
                        obj.mouse_scroll_amount = mouse_state[1][1]

        # Containers that are rotated or have a scroll bar must make use of a surface
        if self.objects_visible_outside_container \
            and not container_has_scroll_bar and self.rot == 0:
            self.call_objects(window, time, mouse_pos, mouse_state, key_state, text_input,
                              is_lame, is_storing_inputs, global_scripts, False, 0)

        else:
            # Create surface matching container's size
            surface = pygame.Surface(self.size).convert_alpha()

            # Draw the area of the window that the surface would be placed on onto the surface
            # so that the surface does not obscure part of the window
            if self.rot == 0:
                surface.blit(window, (
                    -(self.pos[0] - self.size[0] / 2), -(self.pos[1] - self.size[1] / 2)))
            else:
                # Rotate the window around the center coordinates of the container and
                # recalculate the position it needs to be drawn onto the surface
                rotated_window = pygame.transform.rotate(window, -self.rot)
                vector = pygame.math.Vector2(
                    window.get_width() / 2 - self.pos[0],
                    window.get_height() / 2 - self.pos[1]).rotate(self.rot)
                surface.blit(rotated_window, (
                    vector[0] + self.size[0] / 2 - rotated_window.get_width() / 2,
                    vector[1] + self.size[1] / 2 - rotated_window.get_height() / 2))

            # Recalculate mouse position for surface as
            # object positions are changed to be relative to the surface
            mouse_pos = [
                mouse_pos[0] - (self.pos[0] - self.size[0] / 2),
                mouse_pos[1] - (self.pos[1] - self.size[1] / 2)
            ]

            # Update project global scripts before objects
            if hasattr(self, "__is_editor_canvas__") and self.__is_editor_canvas__:
                global_scripts.early_frame_update(time, mouse_pos, mouse_state, key_state)

            self.call_objects(surface, time, mouse_pos, mouse_state, key_state, text_input,
                              is_lame, is_storing_inputs,
                              global_scripts, container_has_scroll_bar, scroll_offset)

            # Update project global scripts after objects
            if hasattr(self, "__is_editor_canvas__") and self.__is_editor_canvas__:
                global_scripts.late_frame_update(time, mouse_pos, mouse_state, key_state)

            # Draws surface to screen
            surface = pygame.transform.rotate(surface, self.rot)
            draw_surface(self, window, surface)

    def call_objects(self, surface, time, mouse_pos, mouse_state, key_state, text_input,
                     is_lame, is_storing_inputs,
                     global_scripts, container_has_scroll_bar, scroll_offset):
        if container_has_scroll_bar:
            scroll_bar_size, object_offset = self.calc_size_scroll_bar()
            # Object offset difference from last frame is added to total object offset
            # Minimum value is zero as creator may want a buffer between the top of the container
            # and the objects within it, therefore objects should never be moved upwards
            self.object_offset = max(self.object_offset + object_offset, 0)
            self.prev_scroll_offset = scroll_offset

            for obj in self.objects:
                # Recalculate size and position for every object as
                # scroll bars are calulated differently to other objects
                pos = [self.size[0] / 2, self.size[1] / 2]
                size = copy.deepcopy(self.size)

                if obj.is_scroll_bar:
                    # The container size given to the scroll bar is changed,
                    # limiting the size of the scroll bar
                    size[1] = scroll_bar_size
                    # Moves the scroll bar to the top of the container
                    pos[1] -= (self.size[1] - size[1]) / 2

                    # Maximum distance the scroll bar can be moved to stay within the container
                    obj.scroll_bar_limit = self.size[1] - size[1]
                else:
                    # Object is moved to take into account the amount the user has scrolled
                    pos[1] += self.object_offset - scroll_offset

                # Calls the object
                obj(surface, time,
                    pos, size, 0, self.opa, mouse_pos, mouse_state, key_state, text_input,
                    is_lame, is_storing_inputs, global_scripts)

        else:
            # Calculates the position of the object depending on whether a surface was used
            if self.objects_visible_outside_container and self.rot == 0:
                pos = copy.deepcopy(self.pos)
            else:
                pos = [self.size[0] / 2, self.size[1] / 2]

            for obj in self.objects:
                # Calls the object
                obj(surface, time,
                    pos, self.size, 0, self.opa, mouse_pos, mouse_state, key_state, text_input,
                    is_lame, is_storing_inputs, global_scripts)

    def calc_size_scroll_bar(self):
        # Min and max y are set to the bounds of the container
        min_y = 0
        max_y = self.size[1]
        cont_min = 0
        cont_max = max_y

        # Checks whether any object within the container goes out of the bounds of the container
        for obj in self.objects:
            # Gets the bounds of the position of the object
            obj_min_y = obj.pos[1] - obj.size[1] / 2 + self.prev_scroll_offset
            obj_max_y = obj.pos[1] + obj.size[1] / 2 + self.prev_scroll_offset
            # If the object's bounds are greater than the container's, redefine min and/or max y
            if obj_min_y < min_y:
                min_y = obj_min_y
            if obj_max_y > max_y:
                max_y = obj_max_y

        # Find the distance the objects protrude out of the top of the container
        object_offset = 0 - min_y

        # Returns size the scroll bar should be and object_offset
        return (self.size[1] ** 2) / (max(max_y - self.object_offset, cont_max) \
               - min(min_y - self.object_offset, cont_min)), object_offset

    def generate_object(self, global_scripts, name, *args):
        if len(args) == 0:
            args = [None]
        for file in global_scripts.object_files:
            # If the name matches the file name
            if file.__name__.split(".")[-1] == name:
                # Get the object types and main class of the file
                object_type = file.object_type
                object_class = file.Main

                # Creates the object inside this container
                self.objects.append(Object(object_type['container'],
                                           object_type['text'],
                                           object_type['image'],
                                           object_type['button'],
                                           object_type['hover_activated'],
                                           object_type['key_activated'],
                                           object_class))
                self.objects[-1].generated_value = args[0]

class Text:
    """
    Methods:
        draw_text(window):
            Draws the object's text to the window
    """

    def draw_text(self, window):
        # Recalculates text as size may have changed
        font = pygame.font.SysFont(self.text_font, round(self.size[1]),
                                   self.text_bold, self.text_italic)
        temp_img = pygame.transform.rotate(font.render(self.text, True, self.text_colour),
                                           self.rot)

        # Aligns text dynamically depending on the text width as this is unpredictable
        self.pos[0] += (self.position_origin[0] - 0.5) * self.size[0]
        self.pos[0] -= (self.position_origin[0] - 0.5) * temp_img.get_width()

        draw_surface(self, window, temp_img)

        # Moves position of object back so that the correct position is passed to child objects
        self.pos[0] -= (self.position_origin[0] - 0.5) * self.size[0]
        self.pos[0] += (self.position_origin[0] - 0.5) * temp_img.get_width()

class Image:
    """
    Attributes:
        img:
            The object's image imported by pygame

    Methods:
        draw_image(window):
            Draws the object's image to the window
    """

    def __init__(self):
        try:
            # convert_alpha allows images without background to remain this way
            self.img = pygame.image.load(self.img_dir).convert_alpha()
        # If the image directory provided does not lead to an image
        except (FileNotFoundError, pygame.error):
            # Create a surface representing the object's image
            self.img = pygame.Surface((1, 1)).convert_alpha()
            # Draw a black rectangle onto the surface so that the object is visible on the screen
            pygame.draw.rect(self.img, self.object_colour, pygame.Rect(0, 0, 1, 1))

        self.prev_img_dir = self.img_dir
        self.prev_obj_col = self.object_colour

    def draw_image(self, window):
        # If the image directory of the object has been changed
        if self.prev_img_dir != self.img_dir or self.prev_obj_col != self.object_colour:
            # Recreate the pygame image
            try:
                self.img = pygame.image.load(self.img_dir).convert_alpha()
            except (FileNotFoundError, pygame.error):
                self.img = pygame.Surface((1, 1)).convert_alpha()
                pygame.draw.rect(self.img, self.object_colour, pygame.Rect(0, 0, 1, 1))

            self.prev_img_dir = self.img_dir
            self.prev_obj_col = self.object_colour

        # Transform the object's image based upon its current attributes
        temp_img = pygame.transform.rotate(pygame.transform.scale(
            self.img, [round(self.size[0]), round(self.size[1])]), self.rot)

        draw_surface(self, window, temp_img)

def draw_surface(self, window, temp_img):
    width = temp_img.get_width()
    height = temp_img.get_height()
    # Position refers to center coordinates, top left corner needed
    x_coord = round(self.pos[0] - width / 2)
    y_coord = round(self.pos[1] - height / 2)

    if self.opa == 1:
        window.blit(temp_img, (x_coord, y_coord))
        return

    # Opacity does not work properly, surface is needed
    # Create surface of the same size as the image
    temp_surface = pygame.Surface((width, height)).convert()
    # Draw the window onto the surface so that the surface does not cover part of it
    temp_surface.blit(window, (-x_coord, -y_coord))
    # Draw the image onto the surface
    temp_surface.blit(temp_img, (0, 0))
    # Change the opacity of the surface
    temp_surface.set_alpha(255 * self.opa)
    # Draw surface onto window
    window.blit(temp_surface, (x_coord, y_coord))

class Button:
    """
    Methods:
        call_clicked(mouse_pos, mouse_state):
            Calls the object's different clicked functions if the object was clicked this frame
            Handles hovering over object logic if the object is both a button and hover_activated
    """

    def __init__(self):
        self.stored_click = [False, False, False]
        self.stored_hover = False

    def call_clicked(self, mouse_pos, mouse_state, is_storing_inputs):
        # Get whether the object's hitbox has collided with the mouse
        collided = hitbox_collision(self, mouse_pos)

        # Scroll bars need to know position of mouse if they are being dragged around
        if collided or (self.is_scroll_bar and self.init_mouse_pos is not None):
            # Call the hoverered_over method from here rather than Hover Activated class
            # to save collision processing
            if hasattr(self, "call_hovered") and callable(self.call_hovered):
                # If the object is storing inputs, save the input
                if is_storing_inputs:
                    self.stored_hover = True
                else:
                    self.hovered_over(mouse_pos)

            # 0 = left mouse button, 1 = middle mouse button, 2 = right mouse button
            if mouse_state[0]:
                # If the object is storing inputs, save the input
                if is_storing_inputs:
                    self.stored_click[0] = True
                else:
                    self.left_clicked(mouse_pos)
            if mouse_state[1][0]:
                # If the object is storing inputs, save the input
                if is_storing_inputs:
                    self.stored_click[1] = True
                else:
                    self.middle_clicked(mouse_pos)
            if mouse_state[2]:
                # If the object is storing inputs, save the input
                if is_storing_inputs:
                    self.stored_click[2] = True
                else:
                    self.right_clicked(mouse_pos)

class Hover_Activated:
    """
    Methods:
        call_hovered(mouse_pos):
            Calls the object's hovered_over method if the object was hovered over this frame
    """

    def __init__(self):
        self.stored_hover = False

    def call_hovered(self, mouse_pos, is_storing_inputs):
        # Get whether the object's hitbox has collided with the mouse
        collided = hitbox_collision(self, mouse_pos)
        if collided:
            # If the object is storing inputs, save the input
            if is_storing_inputs:
                self.stored_hover = True
            else:
                self.hovered_over(mouse_pos)

def hitbox_collision(self, mouse_pos):
    # If the mouse position is within the bounds of the object's hitbox
    if mouse_pos[0] > self.pos[0] - self.size[0] / 2 \
            and mouse_pos[0] < self.pos[0] + self.size[0] / 2 \
            and mouse_pos[1] > self.pos[1] - self.size[1] / 2 \
            and mouse_pos[1] < self.pos[1] + self.size[1] / 2:
        return True
    return False

class Key_Activated:
    """
    Methods:
        call_activated(key_state):
            Calls the object's key_input method for each key that was pressed this frame
            and that should activate the object
    """

    def __init__(self):
        self.stored_keys = []

    def call_activated(self, key_state, text_input, is_storing_inputs):
        # List of keys that activate the object that have been pressed since the last frame
        if hasattr(self, "uses_text_input") and self.uses_text_input:
            activated_keys = [text_input]
        else:
            activated_keys = []

        # Dictionary processing rather than list processing
        for key in self.activation_keys:
            # For each key in the dictionary that has been pressed
            if self.activation_keys[key]:
                # Gets the name given by pygame of the key clicked
                # Length error avoidance
                if len(key) >= 2 and key[:2] == "K_":
                    pygame_key = getattr(pygame, key)
                else:
                    pygame_key = getattr(pygame, f"K_{key}")

                # If the key has been clicked
                if key_state[pygame_key]:
                    # Add the activated key to the list
                    activated_keys.append(key)

        # Call the key input function with each key that has been pressed
        # and should be reacted to, passing the name of the key
        if len(activated_keys) > 0:
            if is_storing_inputs:
                self.stored_keys.extend(activated_keys)
            else:
                self.key_input(activated_keys)

# None classes are throwaways for conditional inheritance
class None1:
    pass
class None2:
    pass
class None3:
    pass
class None4:
    pass
class None5:
    pass
class None6:
    pass
