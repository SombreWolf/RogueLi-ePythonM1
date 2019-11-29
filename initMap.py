from __future__ import print_function
import random
import copy

CHARACTER_TILES = {'stone': ' ',
                   'floor': '.',
                   'wall': '#'}


class Generator:
    """
    generate a basic map
    """

    def __init__(self, width=80, height=70, max_rooms=4, min_room_xy=3, max_room_xy=10,
                 rooms_overlap=False, random_connections=1, random_spurs=5, tiles=CHARACTER_TILES):
        """
        :param width:
        :param height:
        :param max_rooms:
        :param min_room_xy:
        :param max_room_xy:
        :param rooms_overlap:
        :param random_connections:
        :param random_spurs:
        :param tiles:
        """
        self.width = width
        self.height = height
        self.max_rooms = max_rooms
        self.min_room_xy = min_room_xy
        self.max_room_xy = max_room_xy
        self.rooms_overlap = rooms_overlap
        self.random_connections = random_connections
        self.random_spurs = random_spurs
        self.tiles = CHARACTER_TILES
        self.level = []
        self.room_list = []
        self.corridor_list = []
        self.tiles_level = []
        self.tiles_level_copy = []
        self.map_player = []
        self.coord_room_list = []

    def gen_room(self):
        """
        generate the different room [x coord, y coord, x size, y size]
        :return:
        """

        x, y, w, h = 0, 0, 0, 0

        w = random.randint(self.min_room_xy, self.max_room_xy)
        h = random.randint(self.min_room_xy, self.max_room_xy)
        x = random.randint(1, (self.width - w - 1))
        y = random.randint(1, (self.height - h - 1))

        return [x, y, w, h]

    def room_overlapping(self, room, room_list):
        """
        assure that rooms do not overlap
        :param room:
        :param room_list:
        :return:
        """

        x = room[0]
        y = room[1]
        w = room[2]
        h = room[3]

        for current_room in room_list:
            # The rectangles don't overlap if
            # one rectangle's minimum in some dimension
            # is greater than the other's maximum in
            # that dimension.
            if (x < (current_room[0] + current_room[2]) and current_room[0] < (x + w) and
                    y < (current_room[1] + current_room[3]) and current_room[1] < (y + h)):
                return True
        return False

    def corridor_between_points(self, x1, y1, x2, y2, join_type='either'):

        if x1 == x2 and y1 == y2 or x1 == x2 or y1 == y2:
            return [(x1, y1), (x2, y2)]

        else:
            # 2 Corridors
            # NOTE: Never randomly choose a join that will go out of bounds
            # when the walls are added.
            join = None
            if join_type is 'either' and set([0, 1]).intersection(
                    set([x1, x2, y1, y2])):
                join = 'bottom'

            elif join_type is 'either' and set([self.width - 1,
                                                self.width - 2]).intersection(set([x1, x2])) or set(
                [self.height - 1, self.height - 2]).intersection(set([y1, y2])):
                join = 'top'

            elif join_type is 'either':
                join = random.choice(['top', 'bottom'])

            else:
                join = join_type

            if join is 'top':
                return [(x1, y1), (x1, y2), (x2, y2)]

            elif join is 'bottom':
                return [(x1, y1), (x2, y1), (x2, y2)]

    def join_rooms(self, room_1, room_2, join_type='either'):
        """
        Function to joins all the rooms by creating corridors
        :param room_1:
        :param room_2:
        :param join_type:
        :return:
        """
        # sort by the value of x

        sorted_room = [room_1, room_2]
        sorted_room.sort(key=lambda x_y: x_y[0])

        x1 = sorted_room[0][0]
        y1 = sorted_room[0][1]
        w1 = sorted_room[0][2]
        h1 = sorted_room[0][3]

        x1_2 = x1 + w1 - 1
        y1_2 = y1 + h1 - 1

        x2 = sorted_room[1][0]
        y2 = sorted_room[1][1]
        w2 = sorted_room[1][2]
        h2 = sorted_room[1][3]
        x2_2 = x2 + w2 - 1
        y2_2 = y2 + h2 - 1

        # overlapping on x
        if x1 < (x2 + w2) and x2 < (x1 + w1):
            jx1 = random.randint(x2, x1_2)
            jx2 = jx1
            tmp_y = [y1, y2, y1_2, y2_2]
            tmp_y.sort()
            jy1 = tmp_y[1] + 1
            jy2 = tmp_y[2] - 1
            corridors = self.corridor_between_points(jx1, jy1, jx2, jy2)
            self.corridor_list.append(corridors)

        # overlapping on y
        elif y1 < (y2 + h2) and y2 < (y1 + h1):
            if y2 > y1:
                jy1 = random.randint(y2, y1_2)
                jy2 = jy1

            else:
                jy1 = random.randint(y1, y2_2)
                jy2 = jy1

            tmp_x = [x1, x2, x1_2, x2_2]
            tmp_x.sort()
            jx1 = tmp_x[1] + 1
            jx2 = tmp_x[2] - 1
            corridors = self.corridor_between_points(jx1, jy1, jx2, jy2)
            self.corridor_list.append(corridors)



        # no overlap
        else:
            join = None
            if join_type is 'either':
                join = random.choice(['top', 'bottom'])

            else:
                join = join_type

            if join is 'top':
                if y2 > y1:
                    jx1 = x1_2 + 1
                    jy1 = random.randint(y1, y1_2)
                    jx2 = random.randint(x2, x2_2)
                    jy2 = y2 - 1
                    corridors = self.corridor_between_points(jx1, jy1, jx2, jy2, 'bottom')
                    self.corridor_list.append(corridors)

                else:
                    jx1 = random.randint(x1, x1_2)
                    jy1 = y1 - 1
                    jx2 = x2 - 1
                    jy2 = random.randint(y2, y2_2)
                    corridors = self.corridor_between_points(jx1, jy1, jx2, jy2, 'top')
                    self.corridor_list.append(corridors)

            elif join is 'bottom':
                if y2 > y1:
                    jx1 = random.randint(x1, x1_2)
                    jy1 = y1_2 + 1
                    jx2 = x2 - 1
                    jy2 = random.randint(y2, y2_2)
                    corridors = self.corridor_between_points(jx1, jy1, jx2, jy2, 'top')
                    self.corridor_list.append(corridors)

                else:
                    jx1 = x1_2 + 1
                    jy1 = random.randint(y1, y1_2)
                    jx2 = random.randint(x2, x2_2)
                    jy2 = y2_2 + 1
                    corridors = self.corridor_between_points(jx1, jy1, jx2, jy2, 'bottom')
                    self.corridor_list.append(corridors)

    def gen_level(self):
        """
        function to build an empty dungeon, blank the room and corridor lists
        :return:
        """
        for i in range(self.height):
            self.level.append(['stone'] * self.width)

        self.room_list = []
        self.corridor_list = []
        max_iters = self.max_rooms * 5

        for a in range(max_iters):
            tmp_room = self.gen_room()
            if self.rooms_overlap or not self.room_list:
                self.room_list.append(tmp_room)

            else:
                tmp_room = self.gen_room()
                tmp_room_list = self.room_list[:]
                if self.room_overlapping(tmp_room, tmp_room_list) is False:
                    self.room_list.append(tmp_room)

            if len(self.room_list) >= self.max_rooms:
                break

        # connect the rooms
        for a in range(len(self.room_list) - 1):
            self.join_rooms(self.room_list[a], self.room_list[a + 1])

        # do the random joins
        for a in range(self.random_connections):
            room_1 = self.room_list[random.randint(0, len(self.room_list) - 1)]
            room_2 = self.room_list[random.randint(0, len(self.room_list) - 1)]
            self.join_rooms(room_1, room_2)

        # do the spurs
        for a in range(self.random_spurs):
            room_1 = [random.randint(2, self.width - 2), random.randint(2, self.height - 2), 1, 1]
            room_2 = self.room_list[random.randint(0, len(self.room_list) - 1)]
            self.join_rooms(room_1, room_2)

        # fill the map
        # paint rooms
        for room_num, room in enumerate(self.room_list):
            for b in range(room[2]):
                for c in range(room[3]):
                    self.level[room[1] + c][room[0] + b] = 'floor'

        # paint corridors
        for corridor in self.corridor_list:
            x1, y1 = corridor[0]
            x2, y2 = corridor[1]
            for width in range(abs(x1 - x2) + 1):
                for height in range(abs(y1 - y2) + 1):
                    self.level[min(y1, y2) + height][min(x1, x2) + width] = 'floor'

            if len(corridor) == 3:
                x3, y3 = corridor[2]
                for width in range(abs(x2 - x3) + 1):
                    for height in range(abs(y2 - y3) + 1):
                        self.level[min(y2, y3) + height][
                            min(x2, x3) + width] = 'floor'

        # paint the walls
        for row in range(1, self.height - 1):
            for col in range(1, self.width - 1):
                if self.level[row][col] == 'floor':
                    if self.level[row - 1][col - 1] == 'stone':
                        self.level[row - 1][col - 1] = 'wall'

                    if self.level[row - 1][col] == 'stone':
                        self.level[row - 1][col] = 'wall'

                    if self.level[row - 1][col + 1] == 'stone':
                        self.level[row - 1][col + 1] = 'wall'

                    if self.level[row][col - 1] == 'stone':
                        self.level[row][col - 1] = 'wall'

                    if self.level[row][col + 1] == 'stone':
                        self.level[row][col + 1] = 'wall'

                    if self.level[row + 1][col - 1] == 'stone':
                        self.level[row + 1][col - 1] = 'wall'

                    if self.level[row + 1][col] == 'stone':
                        self.level[row + 1][col] = 'wall'

                    if self.level[row + 1][col + 1] == 'stone':
                        self.level[row + 1][col + 1] = 'wall'

    def gen_tiles_level(self):
        """
        function to generate the room which can be display
        :return:
        """
        for row_num, row in enumerate(self.level):
            tmp_tiles = []
            for col_num, col in enumerate(row):
                if col == 'stone':
                    tmp_tiles.append(self.tiles['stone'])

                if col == 'floor':
                    tmp_tiles.append(self.tiles['floor'])

                if col == 'wall':
                    tmp_tiles.append(self.tiles['wall'])

            self.tiles_level.append(''.join(tmp_tiles))

    def get_void_cases(self):
        """
        function to get all the places with no object on it
        :return:
        """
        y = 0
        l_void = []

        for i in self.tiles_level:
            x = 0
            for j in i:
                if j == ".":
                    l_void.append([x, y])
                x += 1
            y += 1

        return l_void

    def init_monster(self, monsters):
        """
        function which will generate the monsters on the map
        :param monsters:
        :return:
        """
        for i in monsters:
            display = i[0].upper()
            x, y = random.choice(self.get_void_cases())
            temp = list(self.tiles_level[y])
            temp[x] = display
            self.tiles_level[y] = "".join(temp)

    def init_exit(self):
        """
        function to create the exit (next level) case on the map
        :return:
        """
        x, y = random.choice(self.get_void_cases())
        temp = list(self.tiles_level[y])
        temp[x] = "▓"
        self.tiles_level[y] = "".join(temp)

    def move_to_player(self, pos, pos2):
        """
        function to realise a movement of the player on the map he saw
        :param pos:
        :param pos2:
        :return:
        """
        if self.tiles_level[pos[1] + pos2[1]][pos[0] + pos2[0]] != '#':
            if pos2[1] == 0:
                temp = list(self.map_player[pos[1]])
                temp[pos[0]], temp[pos[0] + pos2[0]] = temp[pos[0] + pos2[0]], temp[pos[0]]
                self.map_player[pos[1]] = ''.join(temp)

            elif pos2[0] == 0:
                temp = list(self.map_player[pos[1]])
                temp2 = list(self.map_player[pos[1] + pos2[1]])
                temp[pos[0]], temp2[pos[0]] = temp2[pos[0]], temp[pos[0]]
                self.map_player[pos[1]] = ''.join(temp)
                self.map_player[pos[1] + pos2[1]] = ''.join(temp2)
            self.player_enter_room([pos[0] + pos2[0], pos[1] + pos2[1]])
            self.reveal_around_player([pos[0] + pos2[0], pos[1] + pos2[1]])

            return 0

        else:
            return 1

    def new_map_player(self):
        """
        create the map we will display for the player
        :return:
        """
        self.map_player = copy.deepcopy(self.tiles_level)
        c = 0
        for i in self.tiles_level:
            temp = ""
            for j in i:
                temp += " "
            self.map_player[c] = temp
            c += 1

        x, y = random.choice(self.get_void_cases())
        temp = list(self.map_player[y])
        temp[x] = "@"
        self.map_player[y] = "".join(temp)
        self.reveal_around_player([x, y])
        self.player_enter_room([x, y])

        return [x, y]

    def reveal_around_player(self, pos):
        """
        function to reveal the case near the player at each movement
        :param pos:
        :return:
        """
        for i in range(pos[1] - 1, pos[1] + 2):
            temp = list(copy.deepcopy(self.map_player[i]))
            for j in range(pos[0] - 1, pos[0] + 2):
                if not (i == pos[1] and j == pos[0]):
                    temp[j] = self.tiles_level[i][j]
            self.map_player[i] = "".join(temp)

    def reveal_room_coordonates(self, room, pos):
        """
        function to reveal room if the player enter in it
        :param room:
        :param pos:
        :return:
        """
        for i in range(room[1] - 1, room[1] + room[3] + 1):
            temp = list(copy.deepcopy(self.map_player[i]))
            for j in range(room[0] - 1, room[0] + room[2] + 1):
                if not (i == pos[1] and j == pos[0]):
                    temp[j] = self.tiles_level[i][j]

            self.map_player[i] = "".join(temp)

    def coord_room_test(self):
        """
        function to get the coordonnates to test to display the map
        :return:
        """
        self.coord_room_list
        for room in self.room_list:
            coord_room = []
            for i in range(room[1], room[3]):
                coord_room.append([room[0], i])
                coord_room.append([room[0] + room[2] - 1, i])

            for j in range(room[0], room[2]):
                coord_room.append([room[1], j])
                coord_room.append([room[1] + room[3] - 1, j])

            self.coord_room_list.append(coord_room)

    def player_enter_room(self, pos):
        """
        function to test if the player enter a room
        :param pos:
        :return:
        """
        n = 0
        for coord in self.room_list:
            if (coord[0] <= pos[0] < coord[0] + coord[2]) and (coord[1] <= pos[1] < coord[1] + coord[3]):
                self.reveal_room_coordonates(self.room_list[n], pos)

                return True

            n += 1

    def display_map_player(self):
        """
        function to display the map for player
        :return:
        """
        [print(row) for row in self.map_player]

    def display_map(self):
        """
        function to display the map
        :return:
        """
        [print(row) for row in self.tiles_level]


if __name__ == '__main__':

    gen = Generator()

    gen.gen_level()

    gen.gen_tiles_level()
    # print(gen.get_void_cases())
    gen.init_monster(
        ["ghost", "bull", "ghost", "bull", "ghost", "bull", "ghost", "bull", "ghost", "bull", "ghost", "bull", "ghost",
         "bull", "ghost", "bull", "ghost", "bull", "ghost", "bull", "ghost", "bull", "ghost", "bull", "ghost", "bull",
         "ghost", "bull", "ghost", "bull", "ghost", "bull", "ghost", "bull", "ghost", "bull", "ghost", "bull"])
    gen.init_exit()
    coord = gen.new_map_player()
    print(coord)
    while True:
        
        gen.display_map()
        gen.display_map_player()
        x = int(input("Entrer l'avancé selon x"))
        y = int(input("Entrer l'avancé selon y"))
        gen.move_to(coord, [x, y])
        coord = [coord[0] + x, coord[1] + y]
