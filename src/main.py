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

class Bullet(Sprite):
    def __init__(self, image, location, rect):
        Sprite.__init__(self, image, location)
        self.is_firing = False
        self.gunrect = rect
        self.scale(2,2)
        self.moveback()
        self.shot = False
    def fire(self):
        self.is_firing = True
        if self.is_firing:
            if self.rect[1] - self.rect[3] >= 0:
                self.move(0,-10)
            else:
                self.is_firing = False
            if self.rect[1] - self.rect[3] <= 0:
                self.is_firing = False
                return False
        return True
    def set_gunrect(self, rect):
        self.gunrect = rect
        self.moveback()
    def moveback(self):
        self.rect[0] = self.gunrect[0] + 17
        self.rect[1] = self.gunrect[1]
class Flash(Sprite):
    def __init__(self, image, location):
        Sprite.__init__(self, image, location)
    def show():
        pass
class Enemy(Sprite):
    def __init__(self, image, location):
        Sprite.__init__(self, image, location)
        self.hit = False
    def render(self, win):
        if self.hit == False: 
            win.blit(self.image, self.rect)
    def on_hit(self, bullet):
        bullet.is_firing = False
    def set_hit(self,was_hit):
        self.hit = was_hit

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
e1 = Enemy("res/enemy.png", [100,100])
enemies.add(e1)
shooting = False
bullet = Bullet("res/bullet.png", [0,0], player.rect) 

while running:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if player.rect[0] - player.rect[2] <= 0:
        wall_hit_left = True
    else: 
        wall_hit_left = False
    if player.rect[0] + player.rect[2]:
        wall_hit_right = True
    else:
        wall_hit_right = False
    if wall_hit_left == False: 
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: 
            player.move(-4, 0)
            bullet.set_gunrect(player.rect)
    #if wall_hit_right == False:
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]: 
        player.move(4,0)
        bullet.set_gunrect(player.rect)
    if keys[pygame.K_x]:
        shooting = True
    if shooting:
        shooting = bullet.fire()
    elif bullet.rect[1] - bullet.rect[3] <= e1.rect[1] + e1.rect[3] and bullet.rect[0] - bullet.rect[2] <= e1.rect[0] + e1.rect[2]:
        e1.set_hit(True)
        e1.on_hit(bullet)
        bullet.moveback()
    else:
        bullet.moveback()
    window.fill("#222034")
    player.render(window)
    bullet.render(window)
    e1.render(window)
    pygame.display.update()
    clock.tick(60)/1000
