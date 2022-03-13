import pygame as pg
from bullet import Bullet
class Player(pg.sprite.Sprite):
    
    def __init__(self, pos, constraint, speed):
        super().__init__()
        
                
        pg.sprite.Sprite.__init__(self)
    
        self.image = pg.image.load('Assets/images/ship.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed
        self.max_x_constraint = constraint
        
        self.bullets = pg.sprite.Group()
        
        self.bullet_sound = pg.mixer.Sound('Assets/Audio/PP_Cute_Impact_1_2.wav')
        self.bullet_sound.set_volume(0.5)
        self.ready = True
        self.bullet_time = 0
        self.bullet_cooldown = 600
        
        
    def get_input(self):
        user_keys = pg.key.get_pressed()
        if user_keys[pg.K_a]:
            self.rect.x -= self.speed
        elif user_keys[pg.K_d]:
            self.rect.x += self.speed
        if user_keys[pg.K_SPACE] and self.ready:
            self.shoot_bullet()
            self.bullet_sound.play()
            self.ready = False
            self.bullet_time = pg.time.get_ticks() # prepares for recharge
            
    def bullet_recharge(self):
        if not self.ready: 
            current_time = pg.time.get_ticks()
            if current_time - self.bullet_time >= self.bullet_cooldown:
                self.ready = True
         
    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint
            
            
    def shoot_bullet(self):
        self.bullets.add(Bullet(self.rect.center, -8, self.rect.bottom))
        
    def update(self):
        self.get_input()
        self.constraint()
        self.bullet_recharge()
        self.bullets.update()
        