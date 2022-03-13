import pygame as pg
import sys
from alien import Alien
from button import Button
from highscore import Highscore


GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (130, 130, 130)

class LandingPage:

    
    def __init__(self, screen):
        self.aliens = pg.sprite.Group()
        self.image_list = pg.Surface((100,100))
        self.rect = self.image_list.get_rect()
        self.screen = screen
        self.landing_page_finished = False

        headingFont = pg.font.SysFont('Assets/Fonts/Pixeled.ttf', 192)
        subheadingFont = pg.font.SysFont('Assets/Fonts/Pixeled.ttf', 122)
        font = pg.font.SysFont('Assets/Fonts/Pixeled.ttf', 48)
        

        strings = [('SPACE', WHITE, headingFont), ('INVADERS', GREEN, subheadingFont),
                ('= 10 PTS', GREY, font), ('= 20 PTS', GREY, font),
                            ('= 40 PTS', GREY, font), ('= BONUS!', GREY, font)]

        self.texts = [self.get_text(msg=s[0], color=s[1], font=s[2]) for s in strings]

        self.posns = [150, 230]
        alien = [60 * x + 400 for x in range(4)]
        play_high = [x for x in range(650, 760, 80)]
        self.posns.extend(alien)
        self.posns.extend(play_high)

        centerx = self.screen.get_rect().centerx

        self.play_button = Button('Play', 200,50, (500,625), 6, False)
        self.highscore_button = Button('Highscore', 200,50, (500,725), 6, False)
        self.highscore = Highscore()
        
        n = len(self.texts)
        self.rects = [self.get_text_rect(text=self.texts[i], centerx=centerx, centery=self.posns[i]) for i in range(n)]
        
        self.alien_one = Alien(self.screen,"blue", 450, 370 )
        self.alien_two = Alien(self.screen,"red", 450, 434 )
        self.alien_three = Alien(self.screen, "grey", 450, 498 )
        self.ufo = Alien(self.screen,"blue", 450, 560 )
  

    def get_text(self, font, msg, color): return font.render(msg, True, color, BLACK)

    def get_text_rect(self, text, centerx, centery):
        rect = text.get_rect()
        rect.centerx = centerx
        rect.centery = centery
        return rect
    
    def mouse_on_button(self):
        mouse_pos = pg.mouse.get_pos()
        return self.play_button.top_rect.collidepoint(mouse_pos)
    
    def mouse_on_hs_button(self):
        mouse_pos = pg.mouse.get_pos()
        return self.highscore_button.top_rect.collidepoint(mouse_pos)
    
    def check_events(self):
        for event in pg.event.get():
            
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.mouse_on_button():
                    return "PLAYING"
                elif self.mouse_on_hs_button():
                    return "HIGHSCORE"
            user_keys = pg.key.get_pressed()
            if user_keys[pg.K_r]:
                return "HIGHSCORE"
        return "LANDING"

    def show(self):
        self.draw()
        return self.check_events()

    def draw_text(self):
        n = len(self.texts)
        for i in range(n):
            self.screen.blit(self.texts[i], self.rects[i])

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_text()
        self.play_button.drawButton()
        self.highscore_button.drawButton()
        self.alien_one.draw(0)
        self.alien_two.draw(0)
        self.alien_three.draw(0)
        self.ufo.draw(0)

        pg.display.flip()
