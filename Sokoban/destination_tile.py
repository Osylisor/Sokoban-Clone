import pygame
from assetmanager import floor_tile_texture

class Dest_Tile:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 32, 32)

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def render(self, surf):
        surf.blit(floor_tile_texture, (self.x, self.y), pygame.Rect(32, 0, 32, 32))