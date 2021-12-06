import pygame
from game import WIDTH, HEIGHT
from assetmanager import player_texture
import os


move_sfx = pygame.mixer.Sound(os.path.join('Assets', 'Shoot_FX.wav'))
class Player:


    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4
    NUETRAL = 0

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.direction = Player.NUETRAL
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.step_size = 32

    def processInput(self, event):

        #Check for player input and move the player
        if(event.type == pygame.KEYUP):

            #Horizontal movemnt
            if(event.key == pygame.K_RIGHT):
                self.direction = Player.RIGHT
                self.x += self.step_size
                move_sfx.play()
            elif(event.key == pygame.K_LEFT):
                self.direction = Player.LEFT
                self.x -= self.step_size
                move_sfx.play()

            #Vertical movement 
            elif(event.key == pygame.K_UP):
                self.direction = Player.UP
                self.y -= self.step_size
                move_sfx.play()

            elif(event.key == pygame.K_DOWN):
                self.direction = Player.DOWN
                self.y += self.step_size
                move_sfx.play()


    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.check_bounds()


    def render(self, surf):
        surf.blit(player_texture, (self.x, self.y))

    
    def check_bounds(self):

        #Limit the player to the view port
        if(self.x < 0):
            self.x = 0
        
        if(self.x > (WIDTH - self.width)):
            self.x = WIDTH - self.width

        if(self.y < 0):
            self.y = 0
        
        if(self.y > (HEIGHT - self.height)):
             self.y = HEIGHT - self.height