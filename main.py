import pygame, sys, time, random
pygame.init()

screenX, screenY = 640,360
screen  = pygame.display.set_mode((screenX, screenY))
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("sprites/Player/PlayerRocket.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = (320, 330))
        self.bullet_last = 0
        self.dead = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= 16
            if keys[pygame.K_SPACE] or keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
                self.bullet_load(24)
        
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += 16
            if keys[pygame.K_SPACE] or keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
                 self.bullet_load(-16)
        
        if (keys[pygame.K_SPACE] or keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]) and not (keys[pygame.K_a] or keys[pygame.K_LEFT] or keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            self.bullet_load(8)
    
    def player_hit(self):
        got_hit = pygame.sprite.spritecollide(self, alien_group, False)
        if got_hit:
            player_group.remove(self)
            self.dead = 1

    def bullet_load(self, value):
            timer = pygame.time.get_ticks()
            if timer-self.bullet_last >= 256:
                bullet = Bullet(self.rect.x+value, self.rect.y)
                bullet_group.add(bullet)
                self.bullet_last = pygame.time.get_ticks()

    def boundary(self):
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > screenX-16:
             self.rect.x = screenX-16

    def update(self):
         if self.dead == 0:
            self.player_hit()
            self.player_input()
         self.boundary()

class Points():
    def __init__(self):
        self.font = pygame.font.Font(None, 128)
        self.points = 0
        self.text_surface = self.font.render("Points", False, (55,55,55))
        self.points_surface = self.font.render(str(self.points), False, (55,55,55))
        self.last_death = 500
    
    def add(self):
        timer = pygame.time.get_ticks()
        if timer-self.last_death < 500:
            self.points += 4
        elif timer-self.last_death < 850:
            self.points += 2
        elif timer-self.last_death > 850:
            self.points += 1
        self.last_death = pygame.time.get_ticks()
    
    def sub(self):
        self.points -= 1

    def display(self):
        self.points_surface = self.font.render(str(self.points), False, (55,55,55))
        screen.blit(self.points_surface, ((screenX/2)-self.points_surface.get_width()/2, ((screenY/2)-self.points_surface.get_height()/2) - 64))

    def update(self):
        self.display()

class Bullet(pygame.sprite.Sprite):
    def __init__(self,X,Y):
        super().__init__()
        self.image = pygame.image.load("sprites/Player/Bullet.png").convert_alpha()
        self.rect = self.image.get_rect(center = (X, Y))
    
    def destroy(self):
        bullet_group.remove(self)
    
    def bullet_hit(self):
        got_hit = pygame.sprite.spritecollide(self, alien_group, True)
        if got_hit:
            got_hit[0].deplete_health()
            self.destroy()
    
    def boundary(self):
        if self.rect.y < 0:
            self.destroy()

    def update(self):
        self.boundary()
        self.bullet_hit()
        self.rect.y -= 8

class Alien(pygame.sprite.Sprite):
    def __init__(self, row, col, cols):
        super().__init__()
        row = (row*64) + 64
        col = (col*screenX/cols) + (screenX/cols)/2
        self.image = pygame.image.load("sprites/alien/alien1.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = (col, row))
        self.health = 2
        self.cooldown = 1600
        self.last_tick = 1601
        self.move = random.randint(1,6)
        self.roll = True
    
    def kill(self):
        if self.health <= 0:
            alien_group.remove(self)
            points.add()

    def deplete_health(self):
        self.health -= 1
        self.kill()
    
    def boundary(self):
        if self.rect.y > screenY-screenY/6:
            self.kill()
            alien_group.remove(self)
            points.sub()
    
    def pace(self):
        timer = pygame.time.get_ticks()
        if timer-self.last_tick >= self.cooldown:
            self.rect.y += 8
            self.last_tick = pygame.time.get_ticks()
            
    def update(self):
        self.boundary()
        self.pace()

game_active = True

#player
player_group = pygame.sprite.GroupSingle()
player = Player()
player_group.add(player)

#bullet
bullet_group = pygame.sprite.Group()

#Points
points = Points()

#alien
alien_group = pygame.sprite.Group()
rows = 3
cols = 10
for row in range(rows):
    for col in range(cols):
        alien = Alien(row, col, cols)
        alien_group.add(alien)
    cols -= 1

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    if game_active:
        screen.fill(0)
        points.display()
        player_group.draw(screen)
        player.update()
        alien_group.draw(screen)
        alien_group.update()
        bullet_group.draw(screen)
        bullet_group.update()
        

    pygame.display.update()
    clock.tick(24)