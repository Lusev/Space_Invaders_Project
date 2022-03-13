import pygame as pg
import sys
from button import Button

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (130, 130, 130)


class Highscore():
    
    def __init__(self):
        pg.font.init()        
        self.screen = pg.display.set_mode((1200, 800))
        self.background = pg.Surface((1200,800))
        self.highscores = open("highscores.txt", "r")
 
        self.menu_page_finished = False
        
        highscore_headingFont = pg.font.Font('Assets/Fonts/DIGIFIT.TTF', 50)
        highscore_subheadingFont = pg.font.Font('Assets/Fonts/DIGIFIT.TTF', 25)
        highscore_font = pg.font.SysFont('Assets/Fonts/DIGIFIT.TTF', 48)
        
        strings = [('HIGH SCORE', WHITE, highscore_headingFont), ('Player 1', GREEN, highscore_subheadingFont),
             ('HIGH SCORES', GREEN, highscore_font)]
        
        Lines = self.highscores.readlines()
        
        for line in Lines:
            strings.append((line.strip(), GREEN, highscore_subheadingFont))
            
                
        self.texts = [self.get_text(msg=s[0], color=s[1], font=s[2]) for s in strings]
        
        self.posns = [150,200,250,300,350,400,450,500,550]

        
        centerx = self.screen.get_rect().centerx
        
        self.fight_button = Button('Fight Again?', 225, 60, (500, 650), 6, False)
        n = len(self.texts)
        
        self.rects = [self.get_text_rect(text=self.texts[i], centerx=centerx, centery=self.posns[i]) for i in range(n)]
        

    def game_over(self, user_highscore):
        self.highscores = open("highscores.txt", "r")
        
        Lines = self.highscores.readlines()
        overwrite=False
        
        for line in Lines:
            current_score=int(line.strip())
            if current_score<user_highscore:
                overwrite=True
                break
        
        if overwrite:
            high_scores = []
            for line in Lines:
                high_scores.append(int(line.strip()))
            
            high_scores.append(user_highscore)
            high_scores.sort(reverse=True)
            high_scores = high_scores[:len(high_scores)-1]
            
            highscore_headingFont = pg.font.Font('Assets/Fonts/DIGIFIT.TTF', 50)
            highscore_subheadingFont = pg.font.Font('Assets/Fonts/DIGIFIT.TTF', 25)
            highscore_font = pg.font.SysFont('Assets/Fonts/DIGIFIT.TTF', 48)
            
            strings = [('HIGH SCORE', WHITE, highscore_headingFont), ('Player 1', GREEN, highscore_subheadingFont),
                ('HIGH SCORES', GREEN, highscore_font)]
            
            for score in high_scores:
                strings.append((str(score), GREEN, highscore_subheadingFont))
                                    
            self.texts = [self.get_text(msg=s[0], color=s[1], font=s[2]) for s in strings]
            
            self.posns = [150,200,250,300,350,400,450,500,550]
            
            centerx = self.screen.get_rect().centerx
            
            self.fight_button = Button('Fight Again?', 225, 60, (500, 650), 6, False)
            n = len(self.texts)
            
            self.rects = [self.get_text_rect(text=self.texts[i], centerx=centerx, centery=self.posns[i]) for i in range(n)]
            

    def get_text(self, font, msg, color): return font.render(msg, True, color, None)

    def get_text_rect(self, text, centerx, centery):
        rect = text.get_rect()
        rect.centerx = centerx
        rect.centery = centery
        return rect


    def mouse_on_button(self):
        mouse_pos = pg.mouse.get_pos()
        return self.fight_button.top_rect.collidepoint(mouse_pos)
    
    def check_events(self, state):  
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.mouse_on_button():
                        return  "LANDING"
                    
        return "HIGHSCORE"

    def show(self, state):
        self.draw()
        return self.check_events(state) 

    def draw_text(self):
        n = len(self.texts)
        for i in range(n):
            self.screen.blit(self.texts[i], self.rects[i])

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_text()
        self.fight_button.drawButton()
        pg.display.flip()
