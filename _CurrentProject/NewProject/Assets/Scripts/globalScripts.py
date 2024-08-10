"""
The file containing global variables and methods, used in object scripts
"""


import math
import random
import copy


class globalScripts:
    def __init__(self):
        # Required for scroll bars
        self.mouse_pos = [0, 0]
        # Required for text boxes
        self.mouse_state = [False, [False, 0], False]

        # Globals go here
        self.startup = True
        self.my_tribe = None
        self.lookup_index = {
            "world_size" : 0,
            "turn" : 1,
            "turn_progress" : 2,
            "tribes" : 3,
        }

        self.camera_pos = [0, 0]
        self.world_zoom = 100
        self.squash_factor = 0.577

        self.world = []
        self.tribe_terrain = []
        self.regenerate_world = False
        self.display_map = False
        self.update_world = True
        self.delayed_update_world = False

        self.world_size = [0, 0]
        self.turn = 0
        self.turn_progress = 0
        self.tribes = None

        self.type_selected = 0

        self.tile_clicked = False
        self.deselect_tiles = False

        self.slots = []


    # Elapsed time is the time in milliseconds since the last frame
    # Early update is called every frame before any objects are called
    def early_frame_update(self, elapsed_time, mouse_pos, mouse_state, key_state):
        # Required for scroll bars
        self.mouse_pos = mouse_pos
        # Required for text boxes
        self.mouse_state = mouse_state

        if self.startup:
            self.startup = False

            #self.load_world("world1")

            self.generate_world([8, 8], ["Bardur0", "Imperius0"])#, "Kikoo0"])#, "Bardur1", "Oumanji0", "Polaris0", "Xinxi0", "Quetzali0", "Zebasi0", "Vengir0"])
            self.tribe_terrain_generation([8, 8], ["Bardur0", "Imperius0"])#, "Kikoo0"])#, "Bardur1", "Oumanji0", "Polaris0", "Xinxi0", "Quetzali0", "Zebasi0", "Vengir0"])

        if self.regenerate_world:
            self.regenerate_world = False
            self.generate_world([8, 8], ["Bardur0", "Imperius0"])#, "Kikoo0"])#, "Bardur1", "Oumanji0", "Polaris0", "Xinxi0", "Quetzali0", "Zebasi0", "Vengir0"])
            self.tribe_terrain_generation([8, 8], ["Bardur0", "Imperius0"])#, "Kikoo0"])#, "Bardur1", "Oumanji0", "Polaris0", "Xinxi0", "Quetzali0", "Zebasi0", "Vengir0"])

        if self.mouse_state[0]:
            self.deselect_tiles = True

    # Late update is called every frame after all objects have been called
    def late_frame_update(self, elapsed_time, mouse_pos, mouse_state, key_state):
        self.delayed_update_world = self.update_world
        self.update_world = False

        self.delayed_deselect_tiles = self.deselect_tiles
        self.deselect_tiles = False

        self.tile_clicked = False

    # Global methods go here
    def new_tile_clicked(self, tile, distance):
        if distance < self.distance_to_clicked_tile or self.distance_to_clicked_tile == -1:
            self.distance_to_clicked_tile = distance
            self.clicked_tile = tile

    def load_world(self, world_name):
        self.find_current_tribe(world_name)
        self.load_world_data(world_name)

    def find_current_tribe(self, world_name):
        with open("Assets/account_data.txt", "r") as account:
            data = account.read().split("\n")

            games_found = False
            for item in data:
                if games_found:
                    if item[0 : item.index("=")] == world_name:
                        self.my_tribe = item[item.index("=") + 1:]
                        break
                    if item == "":
                        games_found = False
                        break
                if "###" in item and "Games" in item:
                    games_found = True

            if not games_found:
                #report error
                pass

    def load_world_data(self, world_name):
        with open(f"Assets/WorldData/{world_name}.txt", "r") as world:
            data = world.read().split("\n")

            world_size_data = data[self.lookup_index["world_size"]]
            self.world_size[0] = int(world_size_data[0 : world_size_data.index(",")])
            self.world_size[1] = int(world_size_data[world_size_data.index(",") + 1 : world_size_data.index("#") - 1])

            turn_data = data[self.lookup_index["turn"]]
            self.turn = int(turn_data[0 : turn_data.index("#") - 1])

            turn_progress_data = data[self.lookup_index["turn_progress"]]
            self.turn_progress = int(turn_progress_data[0 : turn_progress_data.index("#") - 1])

            tribe_data = data[self.lookup_index["tribes"]]
            self.tribes = tribe_data[0 : tribe_data.index("#") - 1].split(",")

            tile_data_counter = -1
            terrain_counter = -1
            for item in data:
                if tile_data_counter > 0:
                    tile_data_counter -= 1
                    self.world.append(item.split(","))

                    for num in self.world[-1]:
                        num = int(num)
                if "###" in item and "Tile Data" in item:
                    tile_data_counter = self.world_size[1]

                if terrain_counter > 0:
                    terrain_counter -= 1
                    self.tribe_terrain.append(item.split(","))

                    for num in self.tribe_terrain[-1]:
                        num = int(num)
                if "###" in item and "Tribe Terrain Map" in item:
                    terrain_counter = self.world_size[1]

                if tile_data_counter == 0 and terrain_counter == 0:
                    break

    def generate_world(self, size, tribes):
        self.camera_pos = [0, (size[1] - 1) * self.squash_factor * self.world_zoom / 2]

        world = []

        for i in range(size[1]):
            world.append([])
            for _ in range(size[0]):
                world[i].append(0)
        tribe_terrain = copy.deepcopy(world)

        land_proportion = 0
        num_tiles = size[0] * size[1]
        num_list = [1,1,2,2,2,2,3]#[2,2,2,3,3,3,3,3,4,4]

        while land_proportion < 0.5:
            world_copy = copy.deepcopy(world)
            for i, row in enumerate(world):
                for j, val in enumerate(row):
                    if val > 1:
                        world_copy[i][j] = val - 1

                        if val == 2:
                            random_direction = [[-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1]]
                            for _ in range(4):
                                direction = random.choice(random_direction)
                                random_direction.remove(direction)

                                if i + direction[0] >= 0 and i + direction[0] < size[1] and j + direction[1] >= 0 and j + direction[1] < size[0]:
                                    world_copy[i + direction[0]][j + direction[1]] = max(world_copy[i + direction[0]][j + direction[1]], val - 1)

                        else:
                            if i - 1 >= 0:
                                world_copy[i - 1][j] = max(world_copy[i - 1][j], val - 1)
                            if i + 1 < size[1]:
                                world_copy[i + 1][j] = max(world_copy[i + 1][j], val - 1)
                            if j - 1 >= 0:
                                world_copy[i][j - 1] = max(world_copy[i][j - 1], val - 1)
                            if j + 1 < size[0]:
                                world_copy[i][j + 1] = max(world_copy[i][j + 1], val - 1)

            world = copy.deepcopy(world_copy)

            num = random.choice(num_list)
            x = random.randint(0, size[0] - 1)
            y = random.randint(0, size[1] - 1)

            world[y][x] = num

            earth_tally = 0
            for row in world:
                for val in row:
                    if val > 0:
                        earth_tally += 1
            land_proportion = earth_tally / num_tiles

        for i, row in enumerate(world):
            for j, val in enumerate(row):
                if val > 0:
                    if i == 0 or j == 0 or i == size[1] - 1 or j == size[0] - 1:
                        world[i][j] = 1
                    else:
                        world[i][j] = 2
                elif val == 0:
                    while True:
                        if i - 1 >= 0 and world[i - 1][j] > 0:
                            break
                        if i + 1 < size[1] and world[i + 1][j] > 0:
                            break
                        if j - 1 >= 0 and world[i][j - 1] > 0:
                            break
                        if j + 1 < size[0] and world[i][j + 1] > 0:
                            break
                        world[i][j] = -1
                        break

        tile_list = []
        for i in range(size[0] - 2):
            for j in range(size[1] - 2):
                tile_list.append([i + 1, j + 1])

        villiage_spacing = 2
        while len(tile_list) > 0:
            tile = random.choice(tile_list)
            tile_list.remove(tile)

            if world[tile[1]][tile[0]] == 2:
                for i in range(1, villiage_spacing + 1):
                    x = -i
                    y = -i

                    while x < i:
                        x += 1
                        if x + tile[0] > 0 and x + tile[0] < size[0] - 1 and y + tile[1] > 0 and y + tile[1] < size[1] - 1:
                            if world[y + tile[1]][x + tile[0]] == 2:
                                world[y + tile[1]][x + tile[0]] = 1
                    
                    while y < i:
                        y += 1
                        if x + tile[0] > 0 and x + tile[0] < size[0] - 1 and y + tile[1] > 0 and y + tile[1] < size[1] - 1:
                            if world[y + tile[1]][x + tile[0]] == 2:
                                world[y + tile[1]][x + tile[0]] = 1

                    while x > -i:
                        x -= 1
                        if x + tile[0] > 0 and x + tile[0] < size[0] - 1 and y + tile[1] > 0 and y + tile[1] < size[1] - 1:
                            if world[y + tile[1]][x + tile[0]] == 2:
                                world[y + tile[1]][x + tile[0]] = 1
                    
                    while y > -i:
                        y -= 1
                        if x + tile[0] > 0 and x + tile[0] < size[0] - 1 and y + tile[1] > 0 and y + tile[1] < size[1] - 1:
                            if world[y + tile[1]][x + tile[0]] == 2:
                                world[y + tile[1]][x + tile[0]] = 1

        tribe_num = len(tribes)
        for i in range(tribe_num):
            while True:
                x = random.randint(0, size[0] - 1)
                y = random.randint(0, size[1] - 1)

                if tribe_terrain[y][x] == 0:
                    tribe_terrain[y][x] = i + 1
                    break

        self.world = world
        self.tribe_terrain = tribe_terrain
        self.world_size = size

    def tribe_terrain_generation(self, size, tribes):
        tribe_count = copy.deepcopy(tribes)
        override = False
        interation_counter = 0

        uncovered_ratio = 1
        iteration_limit = 0
        one_time = True
        while uncovered_ratio > 0 or interation_counter < iteration_limit:
            interation_counter += 1

            for i in range(len(tribe_count)):
                tribe_count[i] = 0
            tribe_average_tiles = []
            for i in range(len(tribes)):
                tribe_average_tiles.append([0, 0])

            for i, row in enumerate(self.tribe_terrain):
                for j, val in enumerate(row):
                    if val != 0:
                        tribe_count[val - 1] += 1
                        tribe_average_tiles[val - 1][0] += j
                        tribe_average_tiles[val - 1][1] += i

            smallest_count = min(tribe_count)
            smallest_tribe = tribe_count.index(smallest_count) + 1

            if interation_counter > len(tribe_count) * 2:
                override = True

            tribe_terrain_copy = copy.deepcopy(self.tribe_terrain)
            for i, row in enumerate(self.tribe_terrain):
                for j, val in enumerate(row):
                    if val == smallest_tribe:
                        if i - 1 >= 0 and (tribe_terrain_copy[i - 1][j] == 0 or (override and random.random() < 0.2)):
                            tribe_terrain_copy[i - 1][j] = val

                        if i + 1 < size[1] and (tribe_terrain_copy[i + 1][j] == 0 or (override and random.random() < 0.2)):
                            tribe_terrain_copy[i + 1][j] = val

                        if j - 1 >= 0 and (tribe_terrain_copy[i][j - 1] == 0 or (override and random.random() < 0.2)):
                            tribe_terrain_copy[i][j - 1] = val

                        if j + 1 < size[0] and (tribe_terrain_copy[i][j + 1] == 0 or (override and random.random() < 0.2)):
                            tribe_terrain_copy[i][j + 1] = val

            avg_position_smallest_tribe = [round(tribe_average_tiles[smallest_tribe - 1][0] / smallest_count),
                                            round(tribe_average_tiles[smallest_tribe - 1][1] / smallest_count)]
            closest_other_tribe_tile = -1
            tiles_remaining = 0
            counter = 0
            for i, row in enumerate(tribe_terrain_copy):
                for j, val in enumerate(row):
                    if val != smallest_tribe and val != 0:
                        counter+=1
                        distance = math.sqrt((j - avg_position_smallest_tribe[0])**2 + (i - avg_position_smallest_tribe[1])**2)
                        if distance < closest_other_tribe_tile or closest_other_tribe_tile == -1:
                            closest_other_tribe_tile = distance
                    if val == 0:
                        tiles_remaining += 1

            uncovered_ratio = tiles_remaining / (size[0] * size[1])
            if one_time and uncovered_ratio == 0:
                one_time = False
                iteration_limit = interation_counter * 2

            extra_distance = (uncovered_ratio - 0.5) * 0.2
            critical_distance = closest_other_tribe_tile - min(size) * extra_distance
            for i, row in enumerate(tribe_terrain_copy):
                for j, val in enumerate(row):
                    if critical_distance - math.sqrt((j - avg_position_smallest_tribe[0])**2 + (i - avg_position_smallest_tribe[1])**2) > 0:
                        tribe_terrain_copy[i][j] = smallest_tribe

            self.tribe_terrain = copy.deepcopy(tribe_terrain_copy)

        for i in range(len(tribe_count)):
            tribe_count[i] = 0
        tribe_average_tiles = []
        for i in range(len(tribes)):
            tribe_average_tiles.append([0, 0])

        for i, row in enumerate(self.tribe_terrain):
            for j, val in enumerate(row):
                if val != 0:
                    tribe_count[val - 1] += 1
                    tribe_average_tiles[val - 1][0] += j
                    tribe_average_tiles[val - 1][1] += i
        
        for i in range(len(tribe_average_tiles)):
            tribe_average_tiles[i][0] /= tribe_count[i]
            tribe_average_tiles[i][1] /= tribe_count[i]

        min_maxing = True
        for _ in range(50):
            capital_forces = []
            for i in range(len(tribes)):
                capital_forces.append([0, 0])

            closeness_of_capitals = 0
            for i, city in enumerate(tribe_average_tiles):
                for capital in tribe_average_tiles:
                    distance = math.sqrt((city[0] - capital[0])**2 + (city[1] - capital[1])**2)

                    if distance != 0:
                        force = 1 / distance**2
                        capital_forces[i][0] += force * (city[0] - capital[0]) / distance
                        capital_forces[i][1] += force * (city[1] - capital[1]) / distance

                capital_forces[i][0] += 1 / (city[0] + 1)**2 - 1 / (size[0] - city[0])**2
                capital_forces[i][1] += 1 / (city[1] + 1)**2 - 1 / (size[1] - city[1])**2

            max_force = 0
            for force in capital_forces:
                closeness_of_capitals += math.sqrt(force[0]**2 + force[1]**2)
                max_force = max(max_force, abs(force[0]), abs(force[1]))
            for force in capital_forces:
                force[0] /= max_force
                force[1] /= max_force

            for i in range(len(tribe_average_tiles)):
                tile = [min(max(tribe_average_tiles[i][0] + capital_forces[i][0], 0), size[0] - 1),
                        min(max(tribe_average_tiles[i][1] + capital_forces[i][1], 0), size[1] - 1)]

                if self.tribe_terrain[round(tile[1])][round(tile[0])] == i + 1:
                    tribe_average_tiles[i][0] = tile[0]
                    tribe_average_tiles[i][1] = tile[1]

        for i, tile in enumerate(tribe_average_tiles):
            min_dist = -1
            closest_village = []
            for j, row in enumerate(self.world):
                for k, val in enumerate(row):
                    if val == 2:
                        distance = math.sqrt((k - tile[0])**2 + (j - tile[1])**2)
                        if distance < min_dist or min_dist == -1:
                            min_dist = distance
                            closest_village = []
                            closest_village.append([k, j])
                        elif distance == min_dist:
                            closest_village.append([k, j])
            
            village_choice = random.choice(closest_village)
            self.tribe_terrain[village_choice[1]][village_choice[0]] = 0
            self.world[village_choice[1]][village_choice[0]] = 3
