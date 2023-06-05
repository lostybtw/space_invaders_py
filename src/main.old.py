import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.top = location[0]
        self.rect.left = location[1]
        self.size = self.image.get_size()
    
    def render(self,win):
        win.blit(self.image, self.rect)

    def scale(self, scalar_x, scalar_y):
        size_x = self.size[0]
        size_y = self.size[1]
        self.image = pygame.transform.scale(self.image, (int(size_x * scalar_x), int(size_y * scalar_y)))
    
    def move(self, move_x, move_y):
        self.rect[0] += move_x
        self.rect[1] += move_y


class Gun(Sprite):
    def __init__(self, image, location):
        Sprite.__init__(self, image, location)
    def shoot(self,bullet_image, window):
        bullet = Sprite(bullet_image,(self.rect[2], self.rect[3]))
        bullet.scale(3,3)
        if bullet.rect[1] - bullet.rect[3] >=0:
            bullet.render(window)
            bullet.move(0,-10)

class Enemy(Sprite):
    def __init__(self, image, location):
        Sprite.__init__(self, image, location)

pygame.init()
window = pygame.display.set_mode((640,480))
clock = pygame.time.Clock()
running = True
dt = 0
player = Gun("res/gun.png", [100,100])
player.scale(2,2)
wall_hit_left = False
wall_hit_right = False
player.rect[0] = 290
player.rect[1] = 400
enemies = pygame.sprite.Group()
shooting = False

while running:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if player.rect[0] - player.rect[2] <= 0:
        wall_hit_left = True
    else: 
        wall_hit_left = False
    if player.rect[0] + player.rect[2] >= 610:
        wall_hit_right = True
    else:
        wall_hit_right = False
    if wall_hit_left == False: 
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: 
            player.move(-4, 0)
    if wall_hit_right == False:
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: 
            player.move(4,0)
    if keys[pygame.K_x]:
        shooting = True
    if shooting == True:
        player.shoot("res/bullet.png", window)
    window.fill("#222034")
    player.render(window)
    pygame.display.update()
    dt = clock.tick(60)/1000
