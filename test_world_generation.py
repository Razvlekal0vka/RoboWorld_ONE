"""Библиотеки"""
import random

"""Обозначения"""
' '  # пустота
'.'  # поле по которуму может ходить игрок
'#'  # стена
'@'  # стартовая позиция
'East'  # 1
'South'  # 2
'West'  # 3
'North'  # 4

"""Настройка"""
# Настройка стартовых направлений
directions = [[1, 2, 3, 4], ['x']]
# directions = [[1, 2, 3, 4], ['x']] максимальный фарш
# directions = ['r'] - рандомные направления, иначе необходимо передать список
# directions = [['x'], [n]], где n это количество исходных направлений
# directions = [[d1, ...], ['x']], где d1, ... это номера направлений, кодировку смотрите выше, в обозначениях

# Настройка длины коридоров

class Map_generation:
    def __init__(self, size_map, size_room, direc):
        self.WIDTH = self.HEIGHT = self.SIZE = size_map  # размеры карты
        self.generation = True
        self.MAP = []  # слайс карты
        self.SIZE_room = size_room  # размеры начальной комнаты
        self.ends, self.root_ends = [], []
        self.directions = direc  # Настройка стартовых направлений

        self.Filling_the_map_with_emptiness()

    def Filling_the_map_with_emptiness(self):
        """Заполнение карты пустотой"""
        for y in range(self.SIZE):
            line = []
            for x in range(self.SIZE):
                line.append([' '])
            self.MAP.append(line)

        self.Setting_the_starting_location()

    def Setting_the_starting_location(self):
        """Установка стартовой локации"""
        # стартовая локация имеет размеры self.SIZE_room и находится в центре карты
        # устанавливаем координаты комнаты
        x1, y1 = int(self.SIZE / 2 - self.SIZE_room / 2), int(self.SIZE / 2 - self.SIZE_room / 2)
        x2, y2 = int(self.SIZE / 2 + self.SIZE_room / 2), int(self.SIZE / 2 + self.SIZE_room / 2)

        # Проверка параметров создаваймой начальной локации
        if self.directions == ['r'] or not self.directions[0] or not self.directions[1]:
            east = random.randint(0, 1)
            south = random.randint(0, 1)
            west = random.randint(0, 1)
            north = random.randint(0, 1)
            # Если нет дорог, то идем перегенирировать пока не получим хотя бы 1 дорогу
            while east + south + west + north == 0:
                east = random.randint(0, 1)
                south = random.randint(0, 1)
                west = random.randint(0, 1)
                north = random.randint(0, 1)

        elif self.directions[0][0] == 'x':
            number_of_directions = self.directions[1][0]
            if number_of_directions == 0:
                number_of_directions = 1
            east = south = west = north = 0
            while east + south + west + north != number_of_directions:
                east = random.randint(0, 1)
                south = random.randint(0, 1)
                west = random.randint(0, 1)
                north = random.randint(0, 1)

        elif self.directions[1][0] == 'x':
            if 1 not in self.directions[0]:
                east = 0
            else:
                east = 1
            if 2 not in self.directions[0]:
                south = 0
            else:
                south = 1
            if 3 not in self.directions[0]:
                west = 0
            else:
                west = 1
            if 4 not in self.directions[0]:
                north = 0
            else:
                north = 1

        # создаем стены по данным нам координатам и пропиливаем в низ 4 прохода
        if True:
            pc, z = [], 0  # |
            n, n1 = 0, 0  # |
            f, f1 = 1, 1  # | отвечают за определение крайних точек прохода (нужны для генирации проходов)
            for y in range(y1, y2 + 1):  # |
                n = y
                f = 1
                if east == 1:
                    if y >= self.SIZE / 2 + self.SIZE_room * 0.1 + 1 or y < self.SIZE / 2 - self.SIZE_room * 0.1:
                        self.MAP[y - 1][x2 - 1][0], f = '#', 0
                if ((f == 0 and f1 == 1) or (f == 1 and f1 == 0)) and z == 0:
                    z = 1
                elif f == 0 and f1 == 1:
                    pc.append([x2 - 1, n1])
                elif f == 1 and f1 == 0:
                    pc.append([x2 - 1, n])
                f1, n1 = f, n
            self.root_ends.append(pc)

            pc, z = [], 0  # |
            n, n1 = 0, 0  # |
            f, f1 = 1, 1  # | отвечают за определение крайних точек прохода (нужны для генирации проходов)
            for x in range(x1, x2 + 1):
                n = x
                f = 1
                if south == 1:
                    if x >= self.SIZE / 2 + self.SIZE_room * 0.1 + 1 or x < self.SIZE / 2 - self.SIZE_room * 0.1:
                        self.MAP[y2 - 1][x - 1][0], f = '#', 0
                if ((f == 0 and f1 == 1) or (f == 1 and f1 == 0)) and z == 0:
                    z = 1
                elif f == 0 and f1 == 1:
                    pc.append([n1, y2 - 1])
                elif f == 1 and f1 == 0:
                    pc.append([n, y2 - 1])
                f1, n1 = f, n
            self.root_ends.append(pc)

            pc, z = [], 0  # |
            n, n1 = 0, 0  # |
            f, f1 = 1, 1  # | отвечают за определение крайних точек прохода (нужны для генирации проходов)
            for y in range(y1, y2 + 1):  # |
                n = y
                f = 1
                if west == 1:
                    if y >= self.SIZE / 2 + self.SIZE_room * 0.1 + 1 or y < self.SIZE / 2 - self.SIZE_room * 0.1:
                        self.MAP[y - 1][x1 - 1][0], f = '#', 0
                if ((f == 0 and f1 == 1) or (f == 1 and f1 == 0)) and z == 0:
                    z = 1
                elif f == 0 and f1 == 1:
                    pc.append([x1 - 1, n1])
                elif f == 1 and f1 == 0:
                    pc.append([x1 - 1, n])
                f1, n1 = f, n
            self.root_ends.append(pc)

            pc, z = [], 0  # |
            n, n1 = 0, 0  # |
            f, f1 = 1, 1  # | отвечают за определение крайних точек прохода (нужны для генирации проходов)
            for x in range(x1, x2 + 1):
                n = x
                f = 1
                if north == 1:
                    if x >= self.SIZE / 2 + self.SIZE_room * 0.1 + 1 or x < self.SIZE / 2 - self.SIZE_room * 0.1:
                        self.MAP[y1 - 1][x - 1][0], f = '#', 0
                if ((f == 0 and f1 == 1) or (f == 1 and f1 == 0)) and z == 0:
                    z = 1
                elif f == 0 and f1 == 1:
                    pc.append([n1, y1 - 1])
                elif f == 1 and f1 == 0:
                    pc.append([n, y1 - 1])
                f1, n1 = f, n
            self.root_ends.append(pc)

        """Теперь необходимо создавать отдельные локации в четырёх направлениях и проходы до них"""
        for i in self.root_ends:
            print(i)  # крайние точки коридора с одной из четырёх сторон
            # pass
        # self.Leveled_branch_root()

    def Leveled_branch_root(self):
        """Здесь рассматривается направление ветвей"""
        for i in range(4):
            self.Creating_leveled_branches(i + 1)

    def Creating_leveled_branches(self, direction):
        """Здесь происходит генирация ветвей"""
        pass

    def Create_passages(self):
        """Здесь создаются проходы к следующеё ,,комнате,,"""
        pass

    def pr(self):
        for i in self.MAP:
            print(i)


a = Map_generation(100, 10, directions)
