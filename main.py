import pygame
import constant as ct
from os import path

class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(ct.ball)
        self.image.fill(ct.colors['RED'])
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = 5

    def update(self):
        self.rect.x += self.speed

class Ball(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(ct.ball)
        self.image.fill(ct.colors['YELLOW'])
        self.rect = self.image.get_rect()
        self.rect.center = ct.ball_coordinate

    def update(self):
        self.rect.x += 10
        if self.rect.left > ct.window[0]:
            self.rect.right = ct.ball_coordinate[0]
            ct.sun_count += 25
            ct.shoot = 1*ct.num_pies
            print(ct.sun_count)

class Peas(pygame.sprite.Sprite):

    def __init__(self, plant_coordinates=ct.plant_coordinate):
        self.id = 0
        self.cost = ct.cost[self.id]
        self.pies = pygame.image.load(path.join(ct.img_dir, 'pies.png')).convert()
        self.pies_rect = self.pies.get_rect()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(ct.plant)
        self.image.fill(ct.colors['GREEN'])
        self.image.blit(self.pies, self.pies_rect)
        self.rect = self.image.get_rect()
        self.rect.center = plant_coordinates

    def shoot(self, x, y):
        if ct.shoot:
            ct.shoot -= 1
            return Bullet(x, y)
        else:
            return 0

    def update(self):
        if self.rect.left >= 5:
            self.rect.x -= 0
        else:
            self.rect.x += 0

class Zombie(pygame.sprite.Sprite):

    def __init__(self, status=1):
        self.zombie = pygame.image.load((path.join(ct.img_dir, 'zombie.png'))).convert()
        self.zombie_rect = self.zombie.get_rect()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(ct.zombie)
        self.image.blit(self.zombie, self.zombie_rect)
        self.rect = self.image.get_rect()
        self.rect.center = [ct.zombie_spawn_1[0][0], ct.zombie_spawn_1[0][1]]
        self.rect.center = [ct.zombie_spawn_1[ct.zombie_count][0], ct.zombie_spawn_1[ct.zombie_count][1]]
        if status:
            ct.zombie_count += 1

    def update(self):
        self.rect.x -= 0.5
        if self.rect.x <= 56:
            ct.running = False

class GUI:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(ct.window)
        self.clock = pygame.time.Clock()
        self.bullets = pygame.sprite.Group()
        self.zombies = pygame.sprite.Group()
        self.peas = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(Ball())
        self.adding_peas()
        self.adding_zombies()
        self.img_dir = path.join(path.dirname(__file__), ct.img_dir)
        self.background = pygame.image.load(path.join(self.img_dir, 'Background.jpg')).convert()
        self.background_rect = self.background.get_rect()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 16)
        self.sun_count = self.font.render(str(ct.sun_count), False, (0, 0, 0))
        self.background.blit(self.sun_count, dest=(20, 53))
        self.now = 0

    def run(self):
        self.taken = 0
        while ct.running:
            pygame.init()
            pygame.mixer.init()
            pygame.display.flip()
            pygame.display.set_caption('Plants vs Zombies')
            self.killing_plants()
            self.killing_zombies()
            self.cosmetic()
            self.peas_shooting()
            self.spawn()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.pick(event)

    def adding_peas(self, plant_coordinates=ct.plant_coordinate):
        peas = Peas(plant_coordinates)
        self.all_sprites.add(peas)
        self.peas.add(peas)
        print('+ peas')

    def adding_zombies(self, status=1):
        zombie = Zombie(status=status)
        self.zombies.add(zombie)
        self.all_sprites.add(zombie)
        print('+ zombie')

    def adding_bullets(self, x, y):
        bullet = Bullet(x, y)
        self.bullets.add(bullet)
        self.all_sprites.add(bullet)
        print('+ bullet')

    def pick(self, event):
        if self.taken:
            self.plant(event)
        elif event.type == pygame.MOUSEBUTTONUP \
                and (112 < pygame.mouse.get_pos()[0] < 208) \
                and (17 < pygame.mouse.get_pos()[1] < 83) \
                and ct.sun_count >= Peas().cost:
            print('Picked')
            self.taken = Peas().id + 1
            ct.sun_count -= Peas().cost

    def plant(self, event):
        if event.type == pygame.MOUSEBUTTONUP \
                and (0 < pygame.mouse.get_pos()[0] < 996) \
                and (100 < pygame.mouse.get_pos()[1] < 600):
            cur_pos = pygame.mouse.get_pos()
            for i in range(30):
                if ct.bed_boxes_start[i][1] < cur_pos[0] < ct.bed_boxes_end[i][1] \
                        and ct.bed_boxes_start[i][0] < cur_pos[1] < ct.bed_boxes_end[i][0] \
                        and not ct.bed_boxes_centre[i][2]:
                    self.taken = 0
                    self.adding_peas([ct.bed_boxes_centre[i][1], ct.bed_boxes_centre[i][0]])
                    ct.bed_boxes_centre[i][2] += 1
                    ct.num_pies += 1
                elif ct.bed_boxes_centre[i][2]:
                    print('Hi')

    def cosmetic(self):
        self.screen.fill(ct.colors['BLUE'])
        self.screen.blit(self.background, self.background_rect)
        self.all_sprites.draw(self.screen)
        self.clock.tick(ct.FPS)
        self.all_sprites.update()
        self.sun_count = self.font.render(str(ct.sun_count), False, (0, 0, 0))
        self.count_box = pygame.Surface(ct.count_box)
        self.count_box.fill(ct.colors['WHITE'])
        self.background.blit(self.count_box, dest=[15, 43])
        self.background.blit(self.sun_count, dest=(20, 53))

    def spawn(self):
        self.time = pygame.time.get_ticks()
        try:
            if self.time >= self.now + ct.zombie_spawn_1[ct.zombie_count][2]:
                self.adding_zombies()
                self.now = self.time
        except IndexError:
            ct.zombie_count = 0
            if self.time >= self.now + ct.zombie_spawn_1[ct.zombie_count][2]:
                self.adding_zombies()
                self.now = self.time

    def peas_shooting(self):
        if ct.shoot != 0:
            for i in range(30):
                if ct.bed_boxes_centre[i][2]:
                    bullet = Peas().shoot(ct.bed_boxes_centre[i][1], ct.bed_boxes_centre[i][0])
                    if bullet:
                        self.all_sprites.add(bullet)
                        self.bullets.add(bullet)
                        ct.bed_boxes_centre[i][3] = 1

    def killing_plants(self):
        hits = pygame.sprite.groupcollide(self.peas, self.zombies, True, False)
        for hit in hits:
            now = hit.rect
            for i in range(30):
                if ct.bed_boxes_start[i][1] < now[0] < ct.bed_boxes_end[i][1] \
                        and ct.bed_boxes_start[i][0] < now[1] < ct.bed_boxes_end[i][0] \
                        and ct.bed_boxes_centre[i][2]:
                    ct.bed_boxes_centre[i][2] = 0

    def killing_zombies(self):
        pygame.sprite.groupcollide(self.bullets, self.zombies, True, True)


if __name__ == '__main__':
    GUI = GUI()
    GUI.run()