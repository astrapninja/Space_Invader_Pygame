import pygame, sys, time
pygame.init()


screenX, screenY = 640,360
screen  = pygame.display.set_mode((screenX, screenY))
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("sprites/Player/PlayerRocket.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = (320, 330))
        self.bullet_group = pygame.sprite.Group()
        self.bullet_timer = 1


    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= 16
            if keys[pygame.K_SPACE] or keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
                bullet = Bullet(self.rect.x+24, self.rect.y)
                self.bullet_group.add(bullet)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += 16
            if keys[pygame.K_SPACE] or keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
                bullet = Bullet(self.rect.x-16, self.rect.y)
                self.bullet_group.add(bullet)
        if (keys[pygame.K_SPACE] or keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]) and not (keys[pygame.K_a] or keys[pygame.K_LEFT] or keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            
            bullet = Bullet(self.rect.x+8, self.rect.y)
            self.bullet_group.add(bullet)

    def update(self):
         self.player_input()
         self.bullet_group.draw(screen)
         self.bullet_group.update()

class Bullet(pygame.sprite.Sprite):
    def __init__(self,X,Y):
        super().__init__()
        self.image = pygame.image.load("sprites/Player/Bullet.png").convert_alpha()
        self.rect = self.image.get_rect(center = (X, Y))
    
    def update(self):
         self.rect.y -= 8

class Alien(pygame.sprite.Sprite):
    def __init__(self, place):
        x = 32
        x = (place*64) + x 
        super().__init__()
        self.image = pygame.image.load("sprites/alien/alien1.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = (x,100))

game_active = True

#player
player_group = pygame.sprite.GroupSingle()
player = Player()
player_group.add(player)

#alien
alien_group = pygame.sprite.Group()
for place in range(10):
            alien = Alien(place)
            alien_group.add(alien)



while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    if game_active:
        screen.fill(0)
        player_group.draw(screen)
        player.update()
        alien_group.draw(screen)

    pygame.display.update()
    clock.tick(24)