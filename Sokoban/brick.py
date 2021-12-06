import pygame
from assetmanager import brick_texture

class Brick:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.step_size = 32
        self.state = 0



    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
    
    


    def render(self, surf):
        
        surf.blit(brick_texture, (self.x, self.y))