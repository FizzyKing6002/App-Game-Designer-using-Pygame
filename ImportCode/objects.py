import pygame
import math
import copy
from ImportCode import animation

def Object(*args):
    container, text, image, button, hover_activated, key_activated, object_class, *args = args

    class Object(Container if container else None1,
                 Text if text else None2,
                 Image if image else None3,
                 Button if button else None4,
                 Hover_Activated if hover_activated else None5,
                 Key_Activated if key_activated else None6,
                 object_class):
        def __init__(self, *args):
            self.pos = [0, 0]
            self.size = [0, 0]
            self.rot = 0
            self.opa = 1

            if container:
                Container.__init__(self)

            object_class.__init__(self)

            if image and not text:
                Image.__init__(self)

        def __call__(self, window, time,
                     con_pos, con_size, con_rot, con_opa,
                     mouse_pos, mouse_state, key_state, global_scripts):
            if not self.active:
                self.frame_update(global_scripts)
                return

            self.animate(time)
            self.calc_attr(con_pos, con_size, con_rot, con_opa)
            mouse_pos = self.calc_mouse_pos(mouse_pos)

            if hasattr(self, "call_clicked") and callable(self.call_clicked):
                self.call_clicked(mouse_pos, mouse_state)
            elif hasattr(self, "call_hovered") and callable(self.call_hovered):
                self.call_hovered(mouse_pos)

            if hasattr(self, "call_activated") and callable(self.call_activated):
                self.call_activated(key_state)

            self.frame_update(global_scripts)

            if hasattr(self, "draw_self") and callable(self.draw_self):
                self.draw_self(window)

            if hasattr(self, "container_update") and callable(self.container_update):
                self.container_update(window, time,
                                      mouse_pos, mouse_state, key_state, global_scripts)

        def animate(self, time):
            for anim in self.animations:
                if anim[0]:
                    continue

                anim = animation.animate(anim, time)

        def create_animation(self, val, time, anim_type, *args):
            if len(args) == 0:
                args = "x"

            if isinstance(val, list):
                self.animations.append([False, [0, 0], val, 0, time, anim_type, *args])
            else:
                self.animations.append([False, 0, val, 0, time, anim_type, *args])

        def calc_attr(self, con_pos, con_size, con_rot, con_opa):
            pos_mod = copy.deepcopy(self.position_modifiers)
            size_mod = copy.deepcopy(self.size_modifiers)
            rot_mod = copy.deepcopy(self.rotation_modifiers)
            opa_mod = copy.deepcopy(self.opacity_modifiers)

            for anim in self.animations:
                if "%" in anim[-2]:
                    j = 1
                else:
                    j = 0

                if "x" in anim[-2]:
                    i = 0
                elif "y" in anim[-2] and not "opa" in anim[-2]:
                    i = 1
                else:
                    if "pos" in anim[-2]:
                        pos_mod[0][j] += anim[1][0]
                        pos_mod[1][j] += anim[1][1]
                    elif "size" in anim[-2]:
                        size_mod[0][j] += anim[1][0]
                        size_mod[1][j] += anim[1][1]
                    elif "rot" in anim[-2]:
                        rot_mod[j] += anim[1]
                    elif "opa" in anim[-2]:
                        opa_mod[j] += anim[1]
                    continue

                if "pos" in anim[-2]:
                    pos_mod[i][j] += anim[1]
                elif "size" in anim[-2]:
                    size_mod[i][j] += anim[1]

            self.pos = [
                con_pos[0] + con_size[0] * (pos_mod[0][1] - 0.5) + pos_mod[0][0],
                con_pos[1] + con_size[1] * (pos_mod[1][1] - 0.5) + pos_mod[1][0]
            ]
            self.size = [
                max(con_size[0] * size_mod[0][1] + size_mod[0][0], 0),
                max(con_size[1] * size_mod[1][1] + size_mod[1][0], 0)
            ]
            self.rot = con_rot * rot_mod[1] + rot_mod[0]
            self.opa = min(max(con_opa * opa_mod[1] + opa_mod[0], 0), 1)

            self.pos[0] -= (self.position_origin[0] - 0.5) * self.size[0]
            self.pos[1] -= (self.position_origin[1] - 0.5) * self.size[1]

        def calc_mouse_pos(self, mouse_pos):
            if self.rot != 0:
                vector = pygame.math.Vector2(mouse_pos[0] - self.pos[0],
                                             mouse_pos[1] - self.pos[1]).rotate(self.rot)
                mouse_pos = [
                    self.pos[0] + vector[0],
                    self.pos[1] + vector[1]
                ]

            return mouse_pos

    return Object(args)

class Container:
    def __init__(self):
        self.objects = []
        self.object_offset = 0
        self.prev_offset = 0

    def container_update(self, window, time,
                         mouse_pos, mouse_state, key_state, global_scripts):
        self.objects.sort(key=lambda x: x.update_priority, reverse=False)

        container_has_scroll_bar = False
        scroll_offset = 0
        for obj in self.objects:
            if obj.is_scroll_bar:
                container_has_scroll_bar = True

                if obj.size[1] != 0 and self.size[1] - obj.size[1] != 0:
                    scroll_offset = ((self.size[1] ** 2) / obj.size[1] - self.size[1]) \
                        * ((obj.position_modifiers[1][0] + obj.mouse_pos_diff) \
                            / (self.size[1] - obj.size[1]))

        if self.objects_visible_outside_container \
            and not container_has_scroll_bar and self.rot == 0:
            self.call_objects(window, time, mouse_pos, mouse_state, key_state,
                              global_scripts, False, 0)

        else:
            surface = pygame.Surface(self.size).convert_alpha()

            if self.rot == 0:
                surface.blit(window, (
                    -(self.pos[0] - self.size[0] / 2), -(self.pos[1] - self.size[1] / 2)))
            else:
                rotated_window = pygame.transform.rotate(window, -self.rot)
                vector = pygame.math.Vector2(
                    window.get_width() / 2 - self.pos[0],
                    window.get_height() / 2 - self.pos[1]).rotate(self.rot)
                surface.blit(rotated_window, (
                    vector[0] + self.size[0] / 2 - rotated_window.get_width() / 2,
                    vector[1] + self.size[1] / 2 - rotated_window.get_height() / 2))

            mouse_pos = [
                mouse_pos[0] - (self.pos[0] - self.size[0] / 2),
                mouse_pos[1] - (self.pos[1] - self.size[1] / 2)
            ]

            self.call_objects(surface, time, mouse_pos, mouse_state, key_state,
                              global_scripts, container_has_scroll_bar, scroll_offset)

            surface = pygame.transform.rotate(surface, self.rot)
            draw_surface(self, window, surface)

    def iterate_through_objects(self, surface, time, pos, size,
                                mouse_pos, mouse_state, key_state, global_scripts):
        for obj in self.objects:
            obj(surface, time,
                pos, size, self.rot, self.opa,
                mouse_pos, mouse_state, key_state, global_scripts)

    def call_objects(self, surface, time, mouse_pos, mouse_state, key_state,
                     global_scripts, container_has_scroll_bar, scroll_offset):
        if container_has_scroll_bar:
            scroll_bar_size, object_offset = self.calc_size_scroll_bar()
            self.object_offset = max(self.object_offset + object_offset, 0)
            self.prev_offset = scroll_offset

            for obj in self.objects:
                pos = [self.size[0] / 2, self.size[1] / 2]
                size = copy.deepcopy(self.size)

                if obj.is_scroll_bar:
                    size[1] = scroll_bar_size
                    pos[1] -= (self.size[1] - size[1]) / 2
                    obj.scroll_bar_limit = self.size[1] - size[1]
                else:
                    pos[1] += self.object_offset - scroll_offset

                obj(surface, time,
                    pos, size, 0, self.opa,
                    mouse_pos, mouse_state, key_state, global_scripts)

        else:
            if self.objects_visible_outside_container and self.rot == 0:
                pos = copy.deepcopy(self.pos)
            else:
                pos = [self.size[0] / 2, self.size[1] / 2]

            for obj in self.objects:
                obj(surface, time,
                    pos, self.size, 0, self.opa,
                    mouse_pos, mouse_state, key_state, global_scripts)

    def calc_size_scroll_bar(self):
        min_y = 0
        max_y = self.size[1]

        for obj in self.objects:
            obj_min_y = obj.pos[1] - obj.size[1] / 2 + self.prev_offset
            obj_max_y = obj.pos[1] + obj.size[1] / 2 + self.prev_offset
            if obj_min_y < min_y:
                min_y = obj_min_y
            if obj_max_y > max_y:
                max_y = obj_max_y

        object_offset = 0 - min_y

        return (self.size[1] ** 2) / (max_y - min_y), object_offset

class Text:
    def draw_self(self, window):
        font = pygame.font.SysFont(self.text_font, round(self.size[1]),
                                   self.text_bold, self.text_italic)
        temp_img = pygame.transform.rotate(font.render(self.text, True, self.text_colour),
                                           self.rot)

        draw_surface(self, window, temp_img)

class Image:
    def __init__(self):
        self.img = pygame.image.load(self.img_dir).convert_alpha()

    def draw_self(self, window):
        temp_img = pygame.transform.rotate(pygame.transform.scale(
            self.img, [round(self.size[0]), round(self.size[1])]), self.rot)

        draw_surface(self, window, temp_img)

def draw_surface(self, window, temp_img):
    width = temp_img.get_width()
    height = temp_img.get_height()
    x_coord = round(self.pos[0] - width / 2)
    y_coord = round(self.pos[1] - height / 2)

    if self.opa == 1:
        window.blit(temp_img, (x_coord, y_coord))
        return

    temp_surface = pygame.Surface((width, height)).convert()
    temp_surface.blit(window, (-x_coord, -y_coord))
    temp_surface.blit(temp_img, (0, 0))
    temp_surface.set_alpha(255 * self.opa)
    window.blit(temp_surface, (x_coord, y_coord))

class Button:
    def call_clicked(self, mouse_pos, mouse_state):
        collided = hitbox_collision(self, mouse_pos)
        if collided or (self.is_scroll_bar and self.init_mouse_pos is not None):
            if hasattr(self, "call_hovered") and callable(self.call_hovered):
                self.hovered_over(mouse_pos)

            if mouse_state[0]:
                self.left_clicked(mouse_pos)
            if mouse_state[1]:
                self.middle_clicked(mouse_pos)
            if mouse_state[2]:
                self.right_clicked(mouse_pos)

class Hover_Activated:
    def call_hovered(self, mouse_pos):
        collided = hitbox_collision(self, mouse_pos)
        if collided:
            self.hovered_over(mouse_pos)

def hitbox_collision(self, mouse_pos):
    if mouse_pos[0] > self.pos[0] - self.size[0] / 2 \
            and mouse_pos[0] < self.pos[0] + self.size[0] / 2 \
            and mouse_pos[1] > self.pos[1] - self.size[1] / 2 \
            and mouse_pos[1] < self.pos[1] + self.size[1] / 2:
        return True
    return False

class Key_Activated:
    def call_activated(self, key_state):
        for key in self.activation_keys:
            if self.activation_keys[key]:
                if len(key) >= 2 and key[:2] == "K_":
                    exec(f"pygame_key = pygame.{key}",
                         locals(), globals())
                else:
                    exec(f"pygame_key = pygame.K_{key}",
                         locals(), globals())

                if key_state[pygame_key]:
                    self.key_input(key)

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
