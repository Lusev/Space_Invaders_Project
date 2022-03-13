import pygame as pg
import json

class Alien(pg.sprite.Sprite):
    
    def __init__(self, screen, color, x, y):
        super().__init__()
        
        pg.sprite.Sprite.__init__(self)
        file_path = 'Assets/images/alien_json.png'
        json_path = open('Assets/images/alien_json.json')
        json_file = json.load(json_path)
        self.alien_sprites = json_file["frames"]
        self.current_sprite = self.alien_sprites["aliens_grey_1.png"]["frame"]
        self.sprites = []
        self.locations = []
        self.load_sprites(color)
        self.is_alive = True
        self.image = pg.image.load(file_path).convert_alpha()

        self.rect =  pg.Rect(x,y, self.current_sprite["w"], self.current_sprite["h"])
        self.screen = screen
        
        
        if color == 'red': self.value = 100
        elif color == 'blue': self.value = 200
        else:  self.value = 300
    
        
        
    def update(self, direction):
        self.rect.x += direction
        
    def draw(self, total_elapsed_frames):
        location = 0
        if int(total_elapsed_frames % 240) < 120:
            
            if self.is_alive == False:
                location = self.location[2]
            else: 
                location = self.location[0]
        else:
            if self.is_alive == False:
                location = self.location[3]
            else: 
                location = self.location[1]
        self.screen.blit(self.image,self.rect, location)
            
    def load_sprites(self, color):
        sprites= []
        sprites.append(self.alien_sprites[f"aliens_{color}_1.png"])
        sprites.append(self.alien_sprites[f"aliens_{color}_2.png"])
        sprites.append(self.alien_sprites[f"aliens_{color}_death_1.png"])
        sprites.append(self.alien_sprites[f"aliens_{color}_death_2.png"])
        location = []
        location.append(pg.Rect(sprites[0]["frame"]['x'], sprites[0]["frame"]["y"], sprites[0]["frame"]["w"], sprites[0]["frame"]["h"]))
        location.append(pg.Rect(sprites[1]["frame"]["x"], sprites[1]["frame"]["y"], sprites[1]["frame"]["w"], sprites[1]["frame"]["h"]))
        location.append(pg.Rect(sprites[2]["frame"]["x"], sprites[2]["frame"]["y"], sprites[2]["frame"]["w"], sprites[2]["frame"]["h"]))
        location.append(pg.Rect(sprites[3]["frame"]["x"], sprites[3]["frame"]["y"], sprites[3]["frame"]["w"], sprites[3]["frame"]["h"]))
        
        self.sprites = sprites
        self.location = location
        
        
        
class Bonus(pg.sprite.Sprite):
    def __init__(self,side, width):
        super().__init__()
        self.image = pg.image.load('Assets/images/ufo.png').convert_alpha()
        if side == 'right':
            x = width + 50
            self.speed = -3
        else: 
            x = -50
            self.speed = 3
        self.rect = self.image.get_rect(topleft = (x, 80))
        
        
    def update(self):
        self.rect.x += self.speed
        
