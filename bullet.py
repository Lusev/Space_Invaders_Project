import pygame as pg

class Bullet(pg.sprite.Sprite):
    
    def __init__(self, pos, speed, height_limit):
        super().__init__()
        
        self.image = pg.Surface((4,20))
        self.image.fill('blue')
        self.rect = self.image.get_rect(center = pos)

        self.speed = speed
        
        self.height_limit = height_limit
     
        
    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_limit + 50:
            self.kill()
    def update(self):
        self.rect.y += self.speed
        self.destroy()
        

    