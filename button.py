import pygame as pg

class Button:
    def __init__(self, text, width, height, pos, elevation, pressed):
        super().__init__()
        pg.font.init()        

        #Core attributes
        self.pressed = pressed
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]
        
        #top rectangle
        self.top_rect = pg.Rect(pos, (width,height))
        self.top_color = '#475F77'
        
        #bottom rectangle
        self.bottom_rect = pg.Rect(pos, (width, elevation))
        self.bottom_color = '#354B5E'
        
        self.screen = pg.display.set_mode((1200, 800))
        
        #text
        gui_font = pg.font.Font('Assets/Fonts/Pixeled.ttf',20)
        self.text_surf = gui_font.render(text, True, (255,255,255))
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        
    def drawButton(self):
        #elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center
        
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation
        
        pg.draw.rect(self.screen, self.bottom_color, self.bottom_rect, border_radius = 10)
        pg.draw.rect(self.screen, self.top_color, self.top_rect, border_radius = 10)
        self.screen.blit(self.text_surf, self.text_rect)
        self.check_click()
        
    def mouse_on_button(self):
        mouse_pos = pg.mouse.get_pos()
        return self.play_button.rect.collidepoint(mouse_pos)
        
    def check_click(self):
        mouse_pos = pg.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#DB93BB'
            self.bottom_color = '#C85A97'
            if pg.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed == True:
                    self.pressed = False
        else: 
            self.dynamic_elevation = self.elevation
            self.top_color = '#475F77'
            self.bottom_color = '#354B5E'

                