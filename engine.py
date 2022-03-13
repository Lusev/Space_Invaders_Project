import sys
from turtle import Screen
import pygame as pg
from player import Player
import obstacle
from alien import Alien, Bonus
from bullet import Bullet
from random import choice, randint
from landing_page import LandingPage
from highscore import Highscore


class Engine:
    def __init__(self, WIDTH, HEIGHT, title):
        pg.init()
        self.state = "LANDING"
        # Initial setup 
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.x = 0
        self.is_running = True
        self.is_playing = False
        self.bg_color = (200, 200, 200)
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption(title)
        self.font = pg.font.Font('Assets/Fonts/Pixeled.ttf', 20)
        
        # Background
        self.background = pg.image.load('Assets/images/starsbg2.png')
        self.menu_background = pg.image.load('Assets/images/starsbg.png')
        
        # audio
        self.music = pg.mixer.music.load('Assets/Audio/music3.dat')
        pg.mixer.music.set_volume(0.1)
        #self.music.set_volume(0.1) 
        self.bullet_sound = pg.mixer.Sound('Assets/Audio/PP_Cute_Impact_1_2.wav')
        self.bullet_sound.set_volume(0.5)
        self.explosion_sound = pg.mixer.Sound('Assets/Audio/PP_Explosion_1_1.wav')
        self.explosion_sound.set_volume(0.3)
        self.explosion_sound_ship = pg.mixer.Sound('Assets/Audio/PP_Explosion_1_3.wav')
        self.explosion_sound_ship.set_volume(0.3)
        
        
        #Obstacle setup 
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pg.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (WIDTH/ self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start = WIDTH/ 15, y_start = 480 )
        
        # My Player 
        my_player = Player(((WIDTH/2, HEIGHT)), WIDTH, 5)
        self.my_player = pg.sprite.GroupSingle(my_player)
        self.lives=3
        self.live_surface = pg.image.load('Assets/images/ship.png').convert_alpha()
        self.live_width_position = WIDTH - (self.live_surface.get_size()[0]*2 + 20)
        self.score = 0
        
        # bullets
        self.bullets = pg.sprite.Group()
        
        # aliens
        self.aliens = pg.sprite.Group()
        self.alien_bullets = pg.sprite.Group()
        self.alien_setup(rows = 6, cols = 8)
        self.alien_direction = 5

        
        self.bonus = pg.sprite.GroupSingle()
        self.bonus_spawn_time = randint(40, 80)
        #self.setupGame()

        #self.dt = 0
        self.FPS =  60
        self.total_elapsed_frames = 0
        
        self.ALIENLASER = pg.USEREVENT + 1
        self.clock = pg.time.Clock()
        pg.time.set_timer(self.ALIENLASER, 800)
   
       
        self.highscore_page = Highscore()
        self.landing_page = LandingPage(self.screen)
        
   
    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size + 100
                    block = obstacle.Block(self.block_size,(241,79,80),x,y)
                    self.blocks.add(block)
    
    def create_multiple_obstacles(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)
        

    def alien_setup(self, rows, cols, x_distance = 60, y_distance = 48, x_offset = 70, y_offset = 100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                
                
                if row_index == 0:
                    alien_sprite = Alien(self.screen,'blue', x, y)
                elif 1 <= row_index <= 2:
                    alien_sprite = Alien(self.screen,'red', x, y)
                else: 
                    alien_sprite = Alien(self.screen,'grey', x,y)
                self.aliens.add(alien_sprite)

    
    def alien_position_checker(self):
     
        for alien in self.aliens:
            if alien.rect.right >= self.WIDTH:
                self.alien_direction = -5
                self.alien_move_down(3)
            elif alien.rect.left <= 0:
                self.alien_direction = 5
                self.alien_move_down(3)
    
    def alien_move_down(self, distance):
        if self.aliens: 
            for alien in self.aliens.sprites():
                alien.rect.y += distance
    
    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            bullet_sprite = Bullet(random_alien.rect.center, 6, self.HEIGHT)
            self.alien_bullets.add(bullet_sprite)
            self.bullet_sound.play()
            
    def drawButton(self):
        pg.draw.rect(self.screen, self.top_color, self.top_rect)
        self.screen.blit(self.text_surf, self.text_rect)


    def bonus_alien_timer(self):
        self.bonus_spawn_time -= 1
        if self.bonus_spawn_time <= 0:
            self.bonus.add(Bonus(choice(['right', 'left']), self.WIDTH))
            self.bonus_spawn_time = randint(400, 800)
            
    def collision_checks(self):
        if self.my_player.sprite.bullets:
            for bullet in self.my_player.sprite.bullets:
                if pg.sprite.spritecollide(bullet, self.blocks, True):
                    bullet.kill()
                    
                aliens_hit = pg.sprite.spritecollide(bullet, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        alien.is_alive = False
                        self.score += alien.value
                    self.explosion_sound.play()
                    bullet.kill()
                    
                if pg.sprite.spritecollide(bullet, self.bonus, True):
                    self.score += 500
                    bullet.kill()
                    
        if self.alien_bullets:
            for bullet in self.alien_bullets:
                if pg.sprite.spritecollide(bullet, self.blocks, True):
                    bullet.kill()
                if pg.sprite.spritecollide(bullet, self.my_player, False):
                    bullet.kill()              
                    self.lives -= 1
                    self.explosion_sound_ship.play()
                    if self.lives <= 0:
                        print("game over")
                        self.highscore_page.game_over(self.score)
                        self.state= "HIGHSCORE"
                  
        
        if self.aliens:
            for alien in self.aliens:
                pg.sprite.spritecollide(alien, self.blocks, True)
                if pg.sprite.spritecollide(alien, self.my_player, False):
                    pg.quit()
                    sys.exit()
                    
    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_width_position + (live * (self.live_surface.get_size()[0] + 10))
            self.screen.blit(self.live_surface,(x,8))
            
    def display_score(self):
        score_surface = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surface.get_rect(topleft = (10,-10))
        self.screen.blit(score_surface, score_rect)
        
    def victory_message(self):
        if not self.aliens.sprites():
            victory_surace = self.font.render('You won!', False, 'white')
            victory_rect = victory_surace.get_rect(center = (self.WIDTH/2, self.HEIGHT/2))
            self.screen.blit(victory_surace, victory_rect)
    
    def restart_level(self):
        self.lives = 3
        for alien in self.aliens:
            alien.kill()
        for bullet in self.bullets:
            bullet.kill()
        for block in self.blocks:
            block.kill()
        self.aliens.empty()
        self.bullets.empty()
        self.blocks.empty()
        self.alien_setup(rows = 6, cols = 8)
        self.score = 0       
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start=self.WIDTH/ 15, y_start=480)
        

                 
    def update(self):
        self.my_player.update()
        self.alien_position_checker()
        for alien in self.aliens:
            alien.update(self.alien_direction)
        self.alien_bullets.update()
        self.bonus_alien_timer()
        self.bonus.update()
        self.collision_checks()
        
    def draw(self):
        self.my_player.sprite.bullets.draw(self.screen)
        self.my_player.draw(self.screen)
        self.blocks.draw(self.screen)
        for alien in self.aliens:
            alien.draw(self.total_elapsed_frames)
        self.alien_bullets.draw(self.screen)
        self.bonus.draw(self.screen)
        self.display_lives()
        self.display_score()
        self.victory_message()
        
        
    def gameLoop(self):
        
        # audio
        pg.mixer.music.play()
        
        while self.is_running:
            self.screen.fill((0,0,0))

            #print(self.state)
            if self.state == "LANDING": 
                pg.mixer.music.unpause()
                self.state = self.landing_page.show()
                
            elif self.state == "PLAYING":
            
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    if event.type == self.ALIENLASER:
                        self.alien_shoot()

                rel_x = self.x % self.background.get_rect().width
                self.screen.blit(self.background, (rel_x - self.background.get_rect().width, 0))
                if rel_x < self.WIDTH:
                    self.screen.blit(self.background, (rel_x,0))
                self.x += 0.1
            
                self.update()
                self.draw()
   
                pg.display.flip()
                self.clock.tick(self.FPS)
                self.total_elapsed_frames += self.clock.get_fps()
                #print(int(self.total_elapsed_frames % 60))
                
            elif self.state == "HIGHSCORE":
                pg.mixer.music.pause()
                self.state = self.highscore_page.show(self.state)
                self.restart_level()
            else:
                self.is_running =  False
                
def main():
    g = Engine(1200, 800, "spacebois")
    g.gameLoop()
    
if __name__ == '__main__':
    main()
    
