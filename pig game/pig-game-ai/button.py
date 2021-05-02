import pygame

BLACK = (0,0,0)
GREEN = (0,255,0)

# Class for button entity
class Button:
    def __init__(self, x, y, width, height, color=GREEN, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, scr, outline=True):
        if outline:
            pygame.draw.rect(scr, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)

        pygame.draw.rect(scr, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '':
            font = pygame.font.Font('resources/font/consola.ttf', 20)
            text = font.render(self.text, 1, BLACK)
            scr.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):   # Here we take mouse position and compare it
        mouse_x = pos[0]
        mouse_y = pos[1]
        if mouse_x > self.x and mouse_x < self.x + self.width:
            if mouse_y > self.y and mouse_y < self.y + self.height:
                return True
        
        return False
