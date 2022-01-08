import random
from enum import Enum
from PIL import Image


class MAP_ENTRY_TYPE(Enum):
    """Необходим для генирации лабиринтов"""
    MAP_EMPTY = 0,
    MAP_BLOCK = 1,


class WALL_DIRECTION(Enum):
    """Необходим для генирации лабиринтов"""
    WALL_LEFT = 0,
    WALL_UP = 1,
    WALL_RIGHT = 2,
    WALL_DOWN = 3,


class Map:
    def __init__(self):
        self.width = 25
        self.height = 25
        self.map = [[0 for x in range(self.width)] for y in range(self.height)]

    def setMap(self, x, y, value):
        if value == MAP_ENTRY_TYPE.MAP_EMPTY:
            self.map[y][x] = 0
        elif value == MAP_ENTRY_TYPE.MAP_BLOCK:
            self.map[y][x] = 1

    def isMovable(self, x, y):
        return self.map[y][x] != 1

    def isValid(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return True

    def showMap(self):
        map = []
        for row in self.map:
            s = ''
            for entry in row:
                if entry == 0:
                    s += ' '
                elif entry == 1:
                    s += '#'
                else:
                    s += ' X'
            map.append(s)
        maze_map = []
        for i in map:
            line = []
            for j in range(len(i)):
                line.append(i[j])
            maze_map.append(line)
        return maze_map


def recursiveDivision(map, x, y, width, height, wall_value):
    def getWallIndex(start, length):
        assert length >= 3
        wall_index = random.randint(start + 1, start + length - 2)
        if wall_index % 2 == 1:
            wall_index -= 1
        return wall_index

    def generateHoles(map, x, y, width, height, wall_x, wall_y):
        holes = []

        hole_entrys = [(random.randint(x, wall_x - 1), wall_y), (random.randint(wall_x + 1, x + width - 1), wall_y),
                       (wall_x, random.randint(y, wall_y - 1)), (wall_x, random.randint(wall_y + 1, y + height - 1))]
        margin_entrys = [(x, wall_y), (x + width - 1, wall_y), (wall_x, y), (wall_x, y + height - 1)]
        adjacent_entrys = [(x - 1, wall_y), (x + width, wall_y), (wall_x, y - 1), (wall_x, y + height)]
        for i in range(4):
            adj_x, adj_y = (adjacent_entrys[i][0], adjacent_entrys[i][1])
            if map.isValid(adj_x, adj_y) and map.isMovable(adj_x, adj_y):
                map.setMap(margin_entrys[i][0], margin_entrys[i][1], MAP_ENTRY_TYPE.MAP_EMPTY)
            else:
                holes.append(hole_entrys[i])

        ignore_hole = random.randint(0, len(holes) - 1)
        for i in range(0, len(holes)):
            if i != ignore_hole:
                map.setMap(holes[i][0], holes[i][1], MAP_ENTRY_TYPE.MAP_EMPTY)

    if width <= 1 or height <= 1:
        return

    wall_x, wall_y = (getWallIndex(x, width), getWallIndex(y, height))

    for i in range(x, x + width):
        map.setMap(i, wall_y, wall_value)
    for i in range(y, y + height):
        map.setMap(wall_x, i, wall_value)

    generateHoles(map, x, y, width, height, wall_x, wall_y)

    recursiveDivision(map, x, y, wall_x - x, wall_y - y, wall_value)
    recursiveDivision(map, x, wall_y + 1, wall_x - x, y + height - wall_y - 1, wall_value)
    recursiveDivision(map, wall_x + 1, y, x + width - wall_x - 1, wall_y - y, wall_value)
    recursiveDivision(map, wall_x + 1, wall_y + 1, x + width - wall_x - 1, y + height - wall_y - 1, wall_value)


def doRecursiveDivision(map):
    for x in range(0, map.width):
        map.setMap(x, 0, MAP_ENTRY_TYPE.MAP_BLOCK)
        map.setMap(x, map.height - 1, MAP_ENTRY_TYPE.MAP_BLOCK)

    for y in range(0, map.height):
        map.setMap(0, y, MAP_ENTRY_TYPE.MAP_BLOCK)
        map.setMap(map.width - 1, y, MAP_ENTRY_TYPE.MAP_BLOCK)

    recursiveDivision(map, 1, 1, map.width - 2, map.height - 2, MAP_ENTRY_TYPE.MAP_BLOCK)


class Map_generation:
    """Здесь происходит генирация карты"""

    def __init__(self):
        print('Инициализация')
        self.number_of_buildings = 21
        self.number_of_streets = self.number_of_buildings + 1
        self.house = 50
        self.street = 5
        self.border = 1
        self.size_of_the_city = self.number_of_streets * self.street + self.number_of_buildings * self.house + 2 * self.border
        self.map_city = []

        self.map_brown_house = []
        self.map_purple_house = []
        self.map_green_house = []
        self.map_yellow_house = []
        self.map_street = []
        self.crossroads = []
        self.map_border = []

        self.filling_out_the_city_list()

    def filling_out_the_city_list(self):
        print('Заполнение города пустотой')
        for y in range(self.size_of_the_city):
            line = []
            for x in range(self.size_of_the_city):
                line.append(['.'])
            self.map_city.append(line)

        self.filling()

    def filling(self):
        print('Генерация границ карты')
        for x in range(self.size_of_the_city):
            self.map_city[0][x], self.map_city[self.size_of_the_city - 1][x] = ['b'], ['b']
        for y in range(self.size_of_the_city):
            self.map_city[y][0], self.map_city[y][self.size_of_the_city - 1] = ['b'], ['b']

        print('Создание ген. плана застройки и его согласование')
        facades = []
        start_house = 0
        colors = ['brown', 'purple', 'green', 'yellow']
        for _ in range(21):
            street = []
            for __ in range(21):
                color = random.randint(0, 12)
                if 0 <= color <= 3:
                    color = 3
                elif 4 <= color <= 7:
                    color = 2
                elif 8 <= color <= 11:
                    color = 1
                elif color == 12:
                    color = 0
                street.append(colors[color])
            facades.append(street)
            street = []

        x = random.randint(5, 15)
        y = random.randint(5, 15)
        facades[y][x] = 'grey'

        print('Возведение улиц')
        x, y = 6, 1  # горизонтальные
        for _ in range(22):
            for __ in range(21):
                for yy in range(5):
                    for xx in range(50):
                        if yy == 0:
                            self.map_city[y + yy][x + xx] = ['border12', '.']
                        elif yy == 4:
                            self.map_city[y + yy][x + xx] = ['border6', '.']
                        elif (0 < yy < 4 and 0 <= xx <= 2) or (0 < yy < 4 and 47 <= xx <= 49):
                            self.map_city[y + yy][x + xx] = ['transition_g', '.']
                        else:
                            self.map_city[y + yy][x + xx] = ['road_g', '.']
                x += 55
            y += 55
            x = 6

        x, y = 6, 1  # вертикальные
        for _ in range(22):
            for __ in range(21):
                for yy in range(5):
                    for xx in range(50):
                        if yy == 0:
                            self.map_city[x + xx][y + yy] = ['border9', '.']
                        elif yy == 4:
                            self.map_city[x + xx][y + yy] = ['border3', '.']
                        elif (0 < yy < 4 and 0 <= xx <= 2) or (0 < yy < 4 and 47 <= xx <= 49):
                            self.map_city[x + xx][y + yy] = ['transition_v', '.']
                        else:
                            self.map_city[x + xx][y + yy] = ['road_v', '.']
                x += 55
            y += 55
            x = 6

        print('Создание перекрёстков')
        x, y = 1, 1
        for _ in range(22):
            for __ in range(22):
                for yy in range(5):
                    for xx in range(5):
                        if yy == 0 and xx == 0:
                            self.map_city[y + yy][x + xx] = ['c10/11', '.']
                        elif yy == 0 and xx == 4:
                            self.map_city[y + yy][x + xx] = ['c1/2', '.']
                        elif yy == 4 and xx == 4:
                            self.map_city[y + yy][x + xx] = ['c4/5', '.']
                        elif yy == 4 and xx == 0:
                            self.map_city[y + yy][x + xx] = ['c7/8', '.']
                        else:
                            self.map_city[y + yy][x + xx] = ['c', '.']
                x += 55
            y += 55
            x = 1

        print('Строительство зданий')
        x, y = 6, 6
        for _ in range(21):
            for __ in range(21):
                for yy in range(50):
                    for xx in range(50):
                        if facades[_][__] == 'purple':
                            self.map_city[y + yy][x + xx] = ['ph', '#']
                        elif facades[_][__] == 'green':
                            self.map_city[y + yy][x + xx] = ['gh', '#']
                        elif facades[_][__] == 'yellow':
                            self.map_city[y + yy][x + xx] = ['yh', '#']
                        elif facades[_][__] == 'grey':
                            if yy == 0 and (xx < 24 or xx > 27):
                                self.map_city[y + yy][x + xx] = ['sh', '#']
                            elif yy == 49 and (xx < 24 or xx > 27):
                                self.map_city[y + yy][x + xx] = ['sh', '#']
                            elif xx == 0 and (yy < 24 or yy > 27):
                                self.map_city[y + yy][x + xx] = ['sh', '#']
                            elif xx == 49 and (yy < 24 or yy > 27):
                                self.map_city[y + yy][x + xx] = ['sh', '#']
                            elif (yy == 0 and (24 <= xx <= 27)) or (yy == 49 and (24 <= xx <= 27)) or (
                                    xx == 0 and (24 <= yy <= 27)) or (xx == 49 and (24 <= yy <= 27)):
                                self.map_city[y + yy][x + xx] = ['start_passage', '.']
                            else:
                                self.map_city[y + yy][x + xx] = ['start_floor', '.']
                x += 55
            y += 55
            x = 6

        print('Строительство зданий c лабиринтом')
        x, y = 6, 6
        for _ in range(21):
            for __ in range(21):
                map_m = Map()
                doRecursiveDivision(map_m)
                maze = map_m.showMap()
                for yy in range(50):
                    for xx in range(50):
                        if facades[_][__] == 'brown':
                            if yy <= 1 and xx <= 1:
                                self.map_city[y + yy][x + xx] = ['brown_house', '#']
                            else:
                                if xx <= 49 and yy <= 49:
                                    if maze[yy // 2][xx // 2] == '#':
                                        self.map_city[y + yy][x + xx] = ['brown_house', '#']
                                    else:
                                        self.map_city[y + yy][x + xx] = ['brown_house_floor', '.']
                np = random.randint(1, 4)
                rp = random.randint(2, 43)
                if np == 1:
                    self.map_city[x + rp][y + 49] = ['passage', '.']
                    self.map_city[x + rp + 1][y + 49] = ['passage', '.']
                    self.map_city[x + rp + 2][y + 49] = ['passage', '.']
                    self.map_city[x + rp + 3][y + 49] = ['passage', '.']
                elif np == 2:
                    self.map_city[y + 49][x + rp] = ['passage', '.']
                    self.map_city[y + 49][x + rp + 1] = ['passage', '.']
                    self.map_city[y + 49][x + rp + 2] = ['passage', '.']
                    self.map_city[y + 49][x + rp + 3] = ['passage', '.']
                elif np == 3:
                    self.map_city[x + rp][y + 0] = ['passage', '.']
                    self.map_city[x + rp + 1][y + 0] = ['passage', '.']
                    self.map_city[x + rp + 2][y + 0] = ['passage', '.']
                    self.map_city[x + rp + 3][y + 0] = ['passage', '.']
                elif np == 2:
                    self.map_city[y + 0][x + rp] = ['passage', '.']
                    self.map_city[y + 0][x + rp + 1] = ['passage', '.']
                    self.map_city[y + 0][x + rp + 2] = ['passage', '.']
                    self.map_city[y + 0][x + rp + 3] = ['passage', '.']
                x += 55
            x = 6
            y += 55

    def rendering(self):
        print('Создание изображения карты')
        image = Image.new("RGB", (self.size_of_the_city, self.size_of_the_city), (0, 0, 0))
        for y in range(self.size_of_the_city):
            for x in range(self.size_of_the_city):
                coords = (x, y)
                if self.map_city[y][x][0] == 'b':
                    r, g, b = 190, 65, 0
                elif self.map_city[y][x][0] == 'c':
                    r, g, b = 63, 89, 141
                elif self.map_city[y][x][0] == 'c1/2':
                    r, g, b = 63, 89, 191
                elif self.map_city[y][x][0] == 'c4/5':
                    r, g, b = 63, 89, 191
                elif self.map_city[y][x][0] == 'c7/8':
                    r, g, b = 63, 89, 191
                elif self.map_city[y][x][0] == 'c10/11':
                    r, g, b = 63, 89, 191
                elif self.map_city[y][x][0] == 'road_v':
                    r, g, b = 43, 88, 101
                elif self.map_city[y][x][0] == 'road_g':
                    r, g, b = 43, 88, 101
                elif self.map_city[y][x][0] == 'border12':
                    r, g, b = 93, 108, 141
                elif self.map_city[y][x][0] == 'border6':
                    r, g, b = 93, 108, 141
                elif self.map_city[y][x][0] == 'border9':
                    r, g, b = 93, 108, 141
                elif self.map_city[y][x][0] == 'border3':
                    r, g, b = 93, 108, 141
                elif self.map_city[y][x][0] == 'transition_g':
                    r, g, b = 63, 138, 141
                elif self.map_city[y][x][0] == 'transition_v':
                    r, g, b = 63, 138, 141
                elif self.map_city[y][x][0] == 'yh':
                    r, g, b = 141, 76, 63
                elif self.map_city[y][x][0] == 'gh':
                    r, g, b = 115, 141, 63
                elif self.map_city[y][x][0] == 'ph':
                    r, g, b = 138, 81, 117
                elif self.map_city[y][x][0] == 'brown_house':
                    r, g, b = 141, 99, 63
                elif self.map_city[y][x][0] == 'brown_house_floor':
                    r, g, b = 201, 159, 123
                elif self.map_city[y][x][0] == 'sh':
                    r, g, b = 79, 79, 79
                elif self.map_city[y][x][0] == 'passage':
                    r, g, b = 120, 120, 120
                elif self.map_city[y][x][0] == 'start_floor':
                    r, g, b = 200, 200, 200
                else:
                    r, g, b = 0, 0, 0
                image.putpixel(coords, (r, g, b))
        image.save('test_data/' + 'map.png')


level = Map_generation()
level.rendering()
