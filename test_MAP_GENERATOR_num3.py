import random

from PIL import Image


class Map_generation:
    def __init__(self):
        print('Инициализация')
        self.SIZE = 75
        self.wall_len = 5
        self.sea_len = 10
        self.d_len = self.SIZE + self.SIZE + self.wall_len + self.wall_len + self.sea_len + self.sea_len
        self.map_list = []
        self.min_coord = self.max_coord = self.d_len / 2

        self.filling_the_world()

    def filling_the_world(self):
        print('Заполнение мира')
        for y in range(self.d_len):
            line = []
            for x in range(self.d_len):
                line.append(['elem', 'code'])
            self.map_list.append(line)

        self.border_marking()

    def border_marking(self):
        print('Генерируем границы мира')
        xy_wall = []
        xy_floor = []
        xy_sea = []
        r = self.SIZE

        for y in range(self.d_len):
            for x in range(self.d_len):
                if 159999 * self.d_len <= int(
                        ((x - self.d_len / 2) ** 2 + (y - self.d_len / 2) ** 2) ** 2) <= self.d_len * 199999:
                    xy_wall.append([x, y])
                elif int(((x - self.d_len / 2) ** 2 + (y - self.d_len / 2) ** 2) ** 2) >= self.d_len * 199999:
                    xy_sea.append([x, y])

                elif int(((x - self.d_len / 2) ** 2 + (y - self.d_len / 2) ** 2) ** 2) <= 159999 * self.d_len:
                    xy_floor.append([x, y])
                    if x > self.max_coord:
                        self.max_coord = x
                    if x < self.min_coord:
                        self.min_coord = x

        for elem in xy_sea:
            self.map_list[elem[0]][elem[1]][0] = 'sea'
            self.map_list[elem[0]][elem[1]][1] = '.'

        for elem in xy_floor:
            self.map_list[elem[0]][elem[1]][0] = 'floor'
            self.map_list[elem[0]][elem[1]][1] = '.'

        for elem in xy_wall:
            self.map_list[elem[0]][elem[1]][0] = 'wall'
            self.map_list[elem[0]][elem[1]][1] = '#'

        self.creating_a_summer_biome()

    def creating_a_summer_biome(self):
        print('Выращивание летнего биома')
        for y in range(self.d_len):
            for x in range(self.d_len):
                if x == self.d_len / 2 and y == self.d_len / 2:
                    self.lawn_planting(x, y, '@')
                else:
                    if self.map_list[y][x] == ['floor', '.']:
                        n = random.randint(1, 20)
                        if n == 1:
                            self.lawn_planting(x, y, 't')
                        else:
                            self.lawn_planting(x, y, '.')

        self.fence_reassembly()

    def lawn_planting(self, x, y, code):
        n = random.randint(1, 4)
        if n == 1:
            self.map_list[y][x] = ['floor_1', code]
        elif n == 2:
            self.map_list[y][x] = ['floor_2', code]
        elif n == 3:
            self.map_list[y][x] = ['floor_3', code]
        elif n == 4:
            self.map_list[y][x] = ['floor_4', code]

    def fence_reassembly(self):
        print('Перекраска вашего забора')
        for y in range(self.d_len):
            for x in range(self.d_len):
                if self.map_list[y][x][0] == 'wall':
                    self.fence_repainting(x, y, '#')

        self.evaporation_of_the_sea_and_its_planting()

    def fence_repainting(self, x, y, code):
        n = random.randint(1, 2)
        if n == 1:
            self.map_list[y][x] = ['wall_1', code]
        elif n == 2:
            self.map_list[y][x] = ['wall_2', code]

    def evaporation_of_the_sea_and_its_planting(self):
        print('Испарение моря и его засадка')
        for y in range(self.d_len):
            for x in range(self.d_len):
                if self.map_list[y][x][0] == 'sea':
                    n = random.randint(1, 20)
                    if n == 1:
                        self.lawn_planting(x, y, 't')
                    else:
                        self.lawn_planting(x, y, '.')

    def rendering(self):
        print('Создание изображения первоначальной карты')
        image = Image.new("RGB", (self.d_len, self.d_len), (0, 0, 0))
        for y in range(self.d_len):
            for x in range(self.d_len):
                coords = (x, y)
                if self.map_list[y][x][0] == 'wall_1':
                    r, g, b = 71, 31, 0
                elif  self.map_list[y][x][0] == 'wall_2':
                    r, g, b = 81, 41, 0
                elif self.map_list[y][x][0] == 'floor_1':
                    if self.map_list[y][x][1] == 't':
                        r, g, b = 10, 109, 37
                    else:
                        r, g, b = 10, 149, 67
                elif self.map_list[y][x][0] == 'floor_2':
                    if self.map_list[y][x][1] == 't':

                        r, g, b = 10, 109, 37
                    else:
                        r, g, b = 20, 159, 87
                elif self.map_list[y][x][0] == 'floor_3':
                    if self.map_list[y][x][1] == 't':
                        r, g, b = 10, 109, 37
                    else:
                        r, g, b = 30, 169, 97
                elif self.map_list[y][x][0] == 'floor_4':
                    if self.map_list[y][x][1] == 't':
                        r, g, b = 10, 109, 37
                    else:
                        r, g, b = 40, 179, 107
                elif self.map_list[y][x][0] == 'sea':
                    r, g, b = 0, 134, 179
                else:
                    r, g, b = 0, 0, 0

                if self.map_list[y][x][1] == '@':
                    r, g, b = 250, 0, 250
                image.putpixel(coords, (r, g, b))
        image.save('test_data/' + 'map.png')

    def write_in_txt(self):
        print('Сохранение карты')
        with open('test_data/Test_map.txt', 'w') as writing_file:
            for element in self.map_list:
                print(element, file=writing_file)

    def map_level(self):
        return self.map_list


level = Map_generation()
level.rendering()  # Сохраняем изображение карты
level.write_in_txt()  # Сохраняем список в текстовый файл
map_lev = level.map_level()  # Считываем карту
