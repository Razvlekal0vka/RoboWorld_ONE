import os
import sys
import pygame

pygame.init()
size = WIDTH, HEIGHT = 1000, 640
screen = pygame.display.set_mode(size)
FPS = 50
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    # intro_text = []
    fon = pygame.transform.scale(load_image('boot.png'), (WIDTH, HEIGHT))
    name_of_the_game = pygame.transform.scale(load_image('RBWOF.png'), (WIDTH, HEIGHT))
    start_text = pygame.transform.scale(load_image('CIYWETG2.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    screen.blit(name_of_the_game, (0, 0))
    screen.blit(start_text, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    '''for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)'''

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
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
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = pos_x, pos_y


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
tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mario.png')
tile_width = tile_height = STEP = 50

if __name__ == '__main__':
    start_screen()
    camera = Camera()
    running = True
    level = load_level('level1.txt')
    player, level_x, level_y = generate_level(level)
    y, x = player.pos[0] - 1, player.pos[1] + 1
    while running:

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            if x < level_x - 1 and level[y][x + 1] == '.':
                x += 1
                player.rect.x += STEP
        elif keys[pygame.K_a]:
            if x > 0 and level[y][x - 1] == '.':
                x -= 1
                player.rect.x -= STEP
        clock.tick(FPS // 3)

        if keys[pygame.K_w]:
            if y > 0 and level[y - 1][x] == '.':
                y -= 1
                player.rect.y -= STEP
        elif keys[pygame.K_s]:
            if y < level_y - 1 and level[y + 1][x] == '.':
                y += 1
                player.rect.y += STEP
        clock.tick(FPS // 3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            camera.update(player)
            for sprite in all_sprites:
                camera.apply(sprite)
            screen.fill(pygame.Color(0, 0, 0))

            tiles_group.draw(screen)
            player_group.draw(screen)
            clock.tick(FPS)
            pygame.display.flip()

        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)

        screen.fill(pygame.Color(0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    terminate()
