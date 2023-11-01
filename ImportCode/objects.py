import pygame
import math
from ImportCode import animation

def Object(*args):
    container, image, button, hover_activated, key_activated, object_class, *args = args

    class Object(Container if container else None1,
                 Image if image else None2,
                 Button if button else None3,
                 Hover_Activated if hover_activated else None4,
                 Key_Activated if key_activated else None5,
                 object_class):
        def __init__(self, *args):
            self.pos = [0, 0]
            self.size = [0, 0]
            self.rot = 0
            self.opa = 1

            if container:
                Container.__init__(self)

            object_class.__init__(self)

            if image:
                Image.__init__(self)

        def __call__(self, window, time,
                     con_pos, con_size, con_rot, con_opa,
                     mouse_pos, mouse_state, key_state):
            if not self.active:
                self.frame_update(time)
                return

            self.animate(time)
            self.calc_attr(con_pos, con_size, con_rot, con_opa)

            if hasattr(self, "call_clicked") and callable(self.call_clicked):
                self.call_clicked(mouse_pos, mouse_state)
            elif hasattr(self, "call_hovered") and callable(self.call_hovered):
                self.call_hovered(mouse_pos)

            if hasattr(self, "call_activated") and callable(self.call_activated):
                self.call_activated(key_state)

            self.frame_update(time)

            if hasattr(self, "draw_self") and callable(self.draw_self):
                self.draw_self(window)

            if hasattr(self, "call_objects") and callable(self.call_objects):
                self.call_objects(window, time,
                                  mouse_pos, mouse_state, key_state)

        def animate(self, time):
            for anim in self.animations:
                if anim[0]:
                    continue

                anim = animation.animate(anim, time)

        def create_animation(val, time, anim_type, *args):
            if len(args) == 0:
                args = "x"

            if isinstance(val, list):
                return [False, [0, 0], val, 0, time, anim_type, *args]
            else:
                return [False, 0, val, 0, time, anim_type, *args]

        def calc_attr(self, con_pos, con_size, con_rot, con_opa):
            pos_mod = self.position_modifiers
            size_mod = self.size_modifiers
            rot_mod = self.rotation_modifiers
            opa_mod = self.opacity_modifiers

            for anim in self.animations:
                if "move" in anim[-2]:
                    pos_mod[0][0] += anim[1][0]
                    pos_mod[0][1] += anim[1][1]

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

    return Object(args)

class Container:
    def __init__(self):
        self.objects = []

    def call_objects(self, window, time,
                     mouse_pos, mouse_state, key_state):
        for obj in self.objects:
            obj(window, time,
                self.pos, self.size, self.rot, self.opa,
                mouse_pos, mouse_state, key_state)

class Image:
    def __init__(self):
        if self.img_dir is not None:
            self.img = pygame.image.load(self.img_dir).convert_alpha()

    def draw_self(self, window):
        temp_img = pygame.transform.rotate(pygame.transform.scale(
            self.img, [round(self.size[0]), round(self.size[1])]), self.rot)

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
        if hitbox_collision(self, mouse_pos):
            if hasattr(self, "call_hovered") and callable(self.call_hovered):
                self.hovered_over()

            if mouse_state[0]:
                self.left_clicked()
            if mouse_state[1]:
                self.middle_clicked()
            if mouse_state[2]:
                self.right_clicked()

class Hover_Activated:
    def call_hovered(self, mouse_pos):
        if hitbox_collision(self, mouse_pos):
            self.hovered_over()

def hitbox_collision(self, mouse_pos):
    if not self.rot == 0:
        mouse_dist_from_obj_center = math.sqrt(
            (mouse_pos[0] - self.pos[0]) ** 2 + (mouse_pos[1] - self.pos[1]) ** 2)

        if mouse_pos[1] - self.pos[1] == 0:
            mouse_angle_from_obj_center = 90
        else:
            mouse_angle_from_obj_center = math.degrees(math.atan(
                (mouse_pos[0] - self.pos[0]) / (mouse_pos[1] - self.pos[1])))

        if mouse_pos[0] - self.pos[0] < 0:
            mouse_angle_from_obj_center += 180
        mouse_angle_from_obj_center = math.radians(mouse_angle_from_obj_center - self.rot)

        mouse_pos = [
            self.pos[0] + mouse_dist_from_obj_center * math.sin(mouse_angle_from_obj_center),
            self.pos[1] + mouse_dist_from_obj_center * math.cos(mouse_angle_from_obj_center)
        ]

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
