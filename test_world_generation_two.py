import random

from PIL import Image


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
                color = random.randint(0, 3)
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
                        if facades[_][__] == 'brown':
                            self.map_city[y + yy][x + xx] = ['bh', '#']
                        elif facades[_][__] == 'purple':
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
                            elif (yy == 0 and (24 <= xx <= 27)) or (yy == 49 and (24 <= xx <= 27)) or (xx == 0 and (24 <= yy <= 27)) or (xx == 49 and (24 <= yy <= 27)):
                                self.map_city[y + yy][x + xx] = ['passage', '.']
                            else:
                                self.map_city[y + yy][x + xx] = ['start_floor', '.']
                x += 55
            y += 55
            x = 6

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
                elif self.map_city[y][x][0] == 'bh':
                    r, g, b = 141, 99, 63
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


Map = Map_generation()
Map.rendering()
