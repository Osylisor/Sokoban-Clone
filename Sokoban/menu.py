
from pygame import font
from pygame.constants import KEYUP
from State import State
import pygame
from assetmanager import floor_tile_texture
import game
pygame.font.init()
from playstate import Play
import os

font_1 = pygame.font.SysFont("Back to 1982", 32)
font_2 = pygame.font.SysFont("Back to 1982", 128)
selected_sfx = pygame.mixer.Sound(os.path.join('Assets', 'Selected_FX.wav'))

class Menu(State):

    def __init__(self, state_manager):
        super().__init__(state_manager)

    def processInput(self, event):
        
        if(event.type == KEYUP):
            if(event.key == pygame.K_SPACE):
                self.state_manager.set_state(Play(self.state_manager, 1))
                selected_sfx.play()

    def update(self):
        return super().update()

    def render(self, surf):
        self.draw_floor(surf)
        title_text = font_2.render("SOKOBAN", 1, (255, 0, 0))
        info_text = font_1.render("Press space to play", 1, (255, 255, 255))

        surf.blit(title_text, (game.WIDTH/2 - title_text.get_width()/2,  game.HEIGHT/2 - 50))
        surf.blit(info_text, (game.WIDTH/2 - info_text.get_width()/2,  game.HEIGHT/2 + 100))
        return super().render(surf)

    def draw_floor(self, surf):
        
        
        for y in range(int(game.HEIGHT/32)):
            for x in range(int((game.WIDTH)/32)):
                surf.blit(floor_tile_texture, (x * 32, y * 32), 
                pygame.Rect(0, 0, 32, 32))

