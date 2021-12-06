from typing import cast
import pygame
from game import  WIDTH, HEIGHT
from assetmanager import crate_texture

class Crate:

    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.step_size = 32
        self.state = 0
        self.direction = 0


    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.check_bounds()
       

    def render(self, surf):
        surf.blit(crate_texture, (self.x, self.y))

    
    def check_bounds(self):

        #Limit the player to the view port
        if(self.x <= 0):
            #self.x = 0
            self.state = Crate.LEFT
        
        if(self.x >= (WIDTH - self.width)):
            #self.x = WIDTH - self.width
            self.state = Crate.RIGHT

        if(self.y <= 0):
            #self.y = 0
            self.state = Crate.UP
        
        if(self.y >= (HEIGHT - self.height)):
             #self.y = HEIGHT - self.height
             self.state = Crate.DOWN