import os
import random
import sys
from enum import Enum
from random import randint
from tkinter import Image
import pygame
from PIL import Image

pygame.init()
size = WIDTH, HEIGHT = 1000, 640
screen = pygame.display.set_mode(size)
FPS = 60
clock = pygame.time.Clock()


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
                            self.lawn_planting(x, y, 'd')
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
                        self.lawn_planting(x, y, 'd')
                    else:
                        self.lawn_planting(x, y, '.')

        self.territory_marking()

    def territory_marking(self):
        print('Разметка территории')
        n1 = random.randint(1, 4)
        n2 = random.randint(1, 4)
        while n2 == n1:
            n2 = random.randint(1, 4)
        n3 = random.randint(1, 4)
        while n3 == n2 or n3 == n1:
            n3 = random.randint(1, 4)
        n4 = random.randint(1, 4)
        while n4 == n3 or n4 == n2 or n4 == n1:
            n4 = random.randint(1, 4)

        self.burning_flora_and_fauna(n2)
        self.overlay_corruption_on_the_landscape(n3)

    def burning_flora_and_fauna(self, n):
        print('Выжигание флоры и фауны')

        xx = yy = 0
        xy_fire = []

        if n == 1:
            xx, yy = self.d_len / 4, self.d_len / 4
        elif n == 2:
            xx, yy = self.d_len / 4 * 3, self.d_len / 4
        elif n == 3:
            xx, yy = self.d_len / 4 * 3, self.d_len / 4 * 3
        elif n == 4:
            xx, yy = self.d_len / 4, self.d_len / 4 * 3

        for y in range(self.d_len):
            for x in range(self.d_len):
                if int(((x - xx) ** 2 + (y - yy) ** 2) ** 2) <= self.d_len * 159999 / 20:
                    xy_fire.append([x, y])

        for elem in xy_fire:
            x, y = elem[0], elem[1]
            if self.map_list[y][x][0] != 'wall_1' and self.map_list[y][x][0] != 'wall_2':
                n = random.randint(1, 40)
                if n == 1:
                    self.fiery_landscape(x, y, 'd', n)
                elif n == 2:
                    n = 3
                    self.fiery_landscape(x, y, '#', n)
                else:
                    self.fiery_landscape(x, y, '.', n)

    def fiery_landscape(self, x, y, code, n):
        if n == 1:
            self.map_list[y][x] = ['maze_floor_5', code]
        elif n == 2:
            pass
        else:
            n = random.randint(1, 4)
            if n == 1:
                self.map_list[y][x] = ['maze_floor_1', code]
            elif n == 2:
                self.map_list[y][x] = ['maze_floor_2', code]
            elif n == 3:
                self.map_list[y][x] = ['maze_floor_3', code]
            elif n == 4:
                self.map_list[y][x] = ['maze_floor_4', code]

    def overlay_corruption_on_the_landscape(self, n):
        print('Наложение порчи на ландшафт')

        xx = yy = 0
        xy_fire = []

        if n == 1:
            xx, yy = self.d_len / 4, self.d_len / 4
        elif n == 2:
            xx, yy = self.d_len / 4 * 3, self.d_len / 4
        elif n == 3:
            xx, yy = self.d_len / 4 * 3, self.d_len / 4 * 3
        elif n == 4:
            xx, yy = self.d_len / 4, self.d_len / 4 * 3

        for y in range(self.d_len):
            for x in range(self.d_len):
                if int(((x - xx) ** 2 + (y - yy) ** 2) ** 2) <= self.d_len * 159999 / 20:
                    xy_fire.append([x, y])

        for elem in xy_fire:
            x, y = elem[0], elem[1]
            if self.map_list[y][x][0] != 'wall_1' and self.map_list[y][x][0] != 'wall_2':
                n = random.randint(1, 40)
                if n == 1:
                    n = 3
                    self.dark_brick_laying(x, y, 'd', n)
                elif n == 2:
                    n = 3
                    self.dark_brick_laying(x, y, '#', n)
                else:
                    self.dark_brick_laying(x, y, '.', n)

    def dark_brick_laying(self, x, y, code, n):
        if n == 1:
            pass
        elif n == 2:
            n = random.randint(1, 2)
            if n == 1:
                self.map_list[y][x] = ['dark_maze_house_1', '.']
            elif n == 2:
                self.map_list[y][x] = ['dark_maze_house_2', '.']
        else:
            n = random.randint(1, 4)
            if n == 1:
                self.map_list[y][x] = ['dark_maze_floor_1', '.']
            elif n == 2:
                self.map_list[y][x] = ['dark_maze_floor_2', '.']
            elif n == 3:
                self.map_list[y][x] = ['dark_maze_floor_3', '.']
            elif n == 4:
                self.map_list[y][x] = ['dark_maze_floor_4', '.']

    def rendering(self):
        print('Создание изображения первоначальной карты')
        image = Image.new("RGB", (self.d_len, self.d_len), (0, 0, 0))
        for y in range(self.d_len):
            for x in range(self.d_len):
                coords = (x, y)
                if self.map_list[y][x][0] == 'wall_1':
                    r, g, b = 71, 31, 0
                elif self.map_list[y][x][0] == 'wall_2':
                    r, g, b = 81, 41, 0
                elif self.map_list[y][x][0] == 'floor_1':
                    if self.map_list[y][x][1] == 'd':
                        r, g, b = 10, 109, 37
                    else:
                        r, g, b = 10, 149, 67
                elif self.map_list[y][x][0] == 'floor_2':
                    if self.map_list[y][x][1] == 'd':

                        r, g, b = 10, 109, 37
                    else:
                        r, g, b = 20, 159, 87
                elif self.map_list[y][x][0] == 'floor_3':
                    if self.map_list[y][x][1] == 'd':
                        r, g, b = 10, 109, 37
                    else:
                        r, g, b = 30, 169, 97
                elif self.map_list[y][x][0] == 'floor_4':
                    if self.map_list[y][x][1] == 'd':
                        r, g, b = 10, 109, 37
                    else:
                        r, g, b = 40, 179, 107
                elif self.map_list[y][x][0] == 'sea':
                    r, g, b = 0, 134, 179
                elif self.map_list[y][x][0] == 'maze_floor_1':
                    r, g, b = 168, 118, 72
                elif self.map_list[y][x][0] == 'maze_floor_2':
                    r, g, b = 178, 108, 62
                elif self.map_list[y][x][0] == 'maze_floor_3':
                    r, g, b = 188, 98, 52
                elif self.map_list[y][x][0] == 'maze_floor_4':
                    r, g, b = 198, 88, 42
                elif self.map_list[y][x][0] == 'maze_floor_5':
                    r, g, b = 208, 78, 32
                elif self.map_list[y][x][0] == 'dark_maze_floor_1':
                    r, g, b = 114, 102, 108
                elif self.map_list[y][x][0] == 'dark_maze_floor_2':
                    r, g, b = 124, 92, 108
                elif self.map_list[y][x][0] == 'dark_maze_floor_3':
                    r, g, b = 134, 82, 108
                elif self.map_list[y][x][0] == 'dark_maze_floor_4':
                    r, g, b = 144, 72, 108
                elif self.map_list[y][x][0] == 'dark_maze_house_1':
                    r, g, b = 84, 52, 88
                elif self.map_list[y][x][0] == 'dark_maze_house_2':
                    r, g, b = 84, 52, 88
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


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    text = ['Незнакомец: "Нет времени обьяснять, найди фонтаны."',
            'Незнакомец: "Следующие указания поступят позже, возможно..."',
            'Вы: "Ну, ок."']
    fon = pygame.transform.scale(load_image('else/boot.png'), (WIDTH, HEIGHT))
    name_of_the_game = pygame.transform.scale(load_image('else/RBWOF.png'), (WIDTH, HEIGHT))
    start_text = pygame.transform.scale(load_image('else/CIYWETG2.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    screen.blit(name_of_the_game, (0, 0))
    screen.blit(start_text, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 500
    t = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if t != 1:
                    for line in text:
                        string_rendered = font.render(line, True, pygame.Color('orange'))
                        intro_rect = string_rendered.get_rect()
                        text_coord += 10
                        intro_rect.top = text_coord
                        intro_rect.x = 10
                        text_coord += intro_rect.height
                        screen.blit(string_rendered, intro_rect)
                        pygame.display.flip()
                        clock.tick(0.5)
                        t = 1
                elif t == 1:
                    return
        pygame.display.flip()
        clock.tick(FPS)



def load_image(name, color_key=None):
    fullname = os.path.join('test_data/', name)
    if not os.path.isfile(fullname):
        print(f'Файл с изображением \'{fullname}\' не найден')
        sys.exit()
    image = pygame.image.load(fullname)
    if color_key:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "test_data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, enemies, x, y = None, [], None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x][1] == '@':
                Tile(level[y][x][0], x, y)
                new_player = Player(x, y)
            elif level[y][x][1] == 'd':
                Tile(level[y][x][0], x, y)
                n = random.randint(1, 5)
                if n == 5:
                    Tile(str(level[y][x][1]) + str(1), x, y)
                elif 2 <= n <= 4:
                    Tile(str(level[y][x][1]) + str(2), x, y)
                else:
                    Tile(str(level[y][x][1]) + str(2), x, y)
            elif level[y][x][1] == 'e':
                Tile(level[y][x][0], x, y)
                enemies.append(Enemy(x, y))
            elif level[y][x][1] == 'f1':
                Tile(level[y][x][0], x, y)
                Object('fountain', x, y)
            else:
                Tile(level[y][x][0], x, y)
    return new_player, enemies, len(level[0]), len(level)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Object(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(object_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image_lr
        self.rect = self.image.get_rect().move(tile_width * pos_x + 5, tile_height * pos_y)
        self.pos = pos_x, pos_y


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemies_group, all_sprites)
        self.image = enemy_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
object_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()

tile_images = {'wall_1': load_image('world/wall_1.png'),
               'wall_2': load_image('world/wall_2.png'),
               'floor_1': load_image('world/floor_1.png'),
               'floor_2': load_image('world/floor_2.png'),
               'floor_3': load_image('world/floor_3.png'),
               'floor_4': load_image('world/floor_4.png'),
               'yellow_house': load_image('houses/yellow_house/yellow_house.png'),
               'yellow_house_floor': load_image('houses/yellow_house/yellow_house_floor.png'),
               'maze_house': load_image('houses/fire_maze/maze_house.png'),
               'maze_floor_1': load_image('houses/fire_maze/maze_floor_1.png'),
               'maze_floor_2': load_image('houses/fire_maze/maze_floor_2.png'),
               'maze_floor_3': load_image('houses/fire_maze/maze_floor_3.png'),
               'maze_floor_4': load_image('houses/fire_maze/maze_floor_4.png'),
               'maze_floor_5': load_image('houses/fire_maze/maze_floor_5.png'),
               'dark_maze_house_1': load_image('houses/dark_maze/dark_maze_house_1.png'),
               'dark_maze_house_2': load_image('houses/dark_maze/dark_maze_house_2.png'),
               'dark_maze_floor_1': load_image('houses/dark_maze/dark_maze_floor_1.png'),
               'dark_maze_floor_2': load_image('houses/dark_maze/dark_maze_floor_2.png'),
               'dark_maze_floor_3': load_image('houses/dark_maze/dark_maze_floor_3.png'),
               'dark_maze_floor_4': load_image('houses/dark_maze/dark_maze_floor_4.png'),
               'sh': load_image('houses/start_house/sh.png'),
               'passage': load_image('houses/else/passage.png'),
               'start_passage': load_image('houses/else/passage.png'),
               'start_floor': load_image('houses/start_house/start_floor.png'),
               'd1': load_image('world/d1.png'),
               'd2': load_image('world/d2.png'),
               'd3': load_image('world/d3.png'),
               'fountain': load_image('world/fountain.png')}

player_image_lr = load_image('pers/stand_1.png')
standing_player = {'stand_1': load_image('pers/stand_1.png'),
                   'stand_2': load_image('pers/stand_2.png'),
                   'stand_3': load_image('pers/stand_3.png'),
                   'stand_4': load_image('pers/stand_4.png'),
                   'stand_5': load_image('pers/stand_5.png'),
                   'stand_6': load_image('pers/stand_6.png')}

running_player = {'run_1': load_image('pers/run_1.png'),
                  'run_2': load_image('pers/run_2.png'),
                  'run_3': load_image('pers/run_3.png'),
                  'run_4': load_image('pers/run_4.png'),
                  'run_5': load_image('pers/run_5.png'),
                  'run_6': load_image('pers/run_6.png'),
                  'run_7': load_image('pers/run_7.png'),
                  'run_8': load_image('pers/run_8.png'),
                  'run_9': load_image('pers/run_9.png')}

enemy_image = load_image('enemies/base_enemy.png')
tile_width = tile_height = STEP = 50

if __name__ == '__main__':

    def upd_camera():
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)


    def draw():
        screen.fill(pygame.Color(0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        object_group.draw(screen)
        enemies_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS * 4)


    def change_running_pose(lr):
        global running_flag, running_list
        running_flag %= 8
        if lr == 1:
            player.image = pygame.transform.flip(running_player[running_list[running_flag]], True, False)
        else:
            player.image = pygame.transform.flip(running_player[running_list[running_flag]], False, False)
        running_flag += 1


    lev = Map_generation()
    lev.rendering()  # Сохраняем изображение карты
    lev.write_in_txt()
    level = lev.map_level()  # Считываем список
    start_screen()
    camera = Camera()
    running = True
    player, enemies, level_x, level_y = generate_level(level)
    standing_flag, running_flag, lr = 0, 0, 2
    standing_list = ['stand_1', 'stand_2', 'stand_3', 'stand_4', 'stand_5', 'stand_6']
    running_list = ['run_1', 'run_2', 'run_3', 'run_4', 'run_5', 'run_6', 'run_7', 'run_8', 'run_9']
    y, x = player.pos[1], player.pos[0]
    upd_camera()
    while running:

        keys = pygame.key.get_pressed()
        allowed_cells = ['.', 'e', '@', 'f1']

        '''ДВИЖЕНИЕ ИГРОКА'''

        if keys[pygame.K_d] and keys[pygame.K_w]:
            if level[y][x + 1][1] not in allowed_cells and level[y - 1][x][1] in allowed_cells:
                y -= 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.y -= step
                    change_running_pose(2)
                    lr = 2
                    upd_camera()
                    draw()

            elif level[y - 1][x][1] not in allowed_cells and level[y][x + 1][1] in allowed_cells:
                x += 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.x += step
                    change_running_pose(2)
                    lr = 2
                    upd_camera()
                    draw()

            elif level[y - 1][x + 1][1] in allowed_cells:
                x += 1
                y -= 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.x += step
                    player.rect.y -= step
                    change_running_pose(2)
                    lr = 2
                    upd_camera()
                    draw()

        elif keys[pygame.K_d] and keys[pygame.K_s]:
            if level[y][x + 1][1] not in allowed_cells and level[y + 1][x][1] in allowed_cells:
                y += 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.y += step
                    change_running_pose(2)
                    lr = 2
                    upd_camera()
                    draw()

            elif level[y + 1][x][1] not in allowed_cells and level[y][x + 1][1] in allowed_cells:
                x += 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.x += step
                    change_running_pose(2)
                    lr = 2
                    upd_camera()
                    draw()

            elif level[y + 1][x + 1][1] in allowed_cells:
                x += 1
                y += 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.x += step
                    player.rect.y += step
                    change_running_pose(2)
                    lr = 2
                    upd_camera()
                    draw()

        elif keys[pygame.K_a] and keys[pygame.K_s]:
            if level[y + 1][x][1] not in allowed_cells and level[y][x - 1][1] in allowed_cells:
                x -= 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.x -= step
                    change_running_pose(1)
                    lr = 1
                    upd_camera()
                    draw()

            elif level[y][x - 1][1] not in allowed_cells and level[y + 1][x][1] in allowed_cells:
                y += 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.y += step
                    change_running_pose(1)
                    lr = 1
                    upd_camera()
                    draw()

            elif level[y + 1][x - 1][1] in allowed_cells:
                x -= 1
                y += 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.x -= step
                    player.rect.y += step
                    change_running_pose(1)
                    lr = 1
                    upd_camera()
                    draw()

        elif keys[pygame.K_a] and keys[pygame.K_w]:
            if level[y - 1][x][1] not in allowed_cells and level[y][x - 1][1] in allowed_cells:
                x -= 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.x -= step
                    change_running_pose(1)
                    lr = 1
                    upd_camera()
                    draw()

            elif level[y][x - 1][1] not in allowed_cells and level[y - 1][x][1] in allowed_cells:
                y -= 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.y -= step
                    change_running_pose(1)
                    lr = 1
                    upd_camera()
                    draw()

            elif level[y - 1][x - 1][1] in allowed_cells:
                x -= 1
                y -= 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.x -= step
                    player.rect.y -= step
                    change_running_pose(1)
                    lr = 1
                    upd_camera()
                    draw()

        elif keys[pygame.K_d]:
            if level[y][x + 1][1] in allowed_cells:
                x += 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.x += step
                    change_running_pose(2)
                    lr = 2
                    upd_camera()
                    draw()

        elif keys[pygame.K_a]:
            if level[y][x - 1][1] in allowed_cells:
                x -= 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.x -= step
                    change_running_pose(1)
                    lr = 1
                    upd_camera()
                    draw()

        elif keys[pygame.K_w]:
            if level[y - 1][x][1] in allowed_cells:
                y -= 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.y -= step
                    if lr == 2:
                        change_running_pose(2)
                    else:
                        change_running_pose(1)
                    upd_camera()
                    draw()

        elif keys[pygame.K_s]:
            if level[y + 1][x][1] in allowed_cells:
                y += 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.y += step
                    if lr == 2:
                        change_running_pose(2)
                    else:
                        change_running_pose(1)
                    upd_camera()
                    draw()

        elif keys[pygame.K_s] == False and keys[pygame.K_w] == False \
                and keys[pygame.K_a] == False and keys[pygame.K_d] == False:
            standing_flag %= 5
            if lr == 2:
                player.image = pygame.transform.flip(standing_player[standing_list[standing_flag]], False, False)
            else:
                player.image = pygame.transform.flip(standing_player[standing_list[standing_flag]], True, False)
            standing_flag += 1
            clock.tick(FPS // 8)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            upd_camera()
        draw()
    terminate()
