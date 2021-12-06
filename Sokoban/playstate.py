import pygame
from State import State
from game import WIDTH, HEIGHT
import menu
from player import Player
from crate import Crate
from brick import Brick
from destination_tile import Dest_Tile
import os
from assetmanager import floor_tile_texture, border_texture




pygame.font.init()
pygame.mixer.init()

font = pygame.font.SysFont("Back to 1982", 32)
font_2 = pygame.font.SysFont("Back to 1982", 23)
font_3 = pygame.font.SysFont("Back to 1982", 128)

#Load sound effects

selected_sfx = pygame.mixer.Sound(os.path.join('Assets', 'Selected_FX.wav'))


class Play(State):

#Initialize everything
    def __init__(self, state_manager, level):
        #initialize varibales here
        super().__init__(state_manager)
        self.player = None
        self.bricks = []
        self.crates = []
        self.dest_tiles = []
        self.count = 0
        self.level = level
        self.leve_cleared = False
        self.minutes = 1
        self.second = 59
        self.timer = 0
        self.is_game_over = False
        self.leve_paused = False

        self.pause_menu_index = 0

        #call fuctions here
        self.load_level(level)
       
#Process player input
    def processInput(self, event):
        if((self.leve_cleared != True) and (self.is_game_over) != True and not( self.leve_paused)): 
            self.player.processInput(event)

        #Go to the menu if it's game over
        if(self.is_game_over):
            if(event.type == pygame.KEYUP):
                if(event.key == pygame.K_SPACE):
                    self.state_manager.set_state(menu.Menu(self.state_manager))
                    selected_sfx.play(0)

        #Go to the next level or menu when the game is completed
        if(self.leve_cleared):
            if(event.type == pygame.KEYUP):
                if(event.key == pygame.K_SPACE):
                    if(self.level < 10):
                        self.level += 1
                        sm = self.state_manager
                        self.state_manager.set_state(Play(sm, self.level))
                        selected_sfx.play(0)
                    else:
                        sm = self.state_manager
                        self.state_manager.set_state(menu.Menu(sm))
                        selected_sfx.play(0)

        #Puase or unpause the game
        if((self.leve_cleared != True) and not(self.is_game_over)):
            if(event.type == pygame.KEYUP):
                if(event.key == pygame.K_ESCAPE):
                    self.leve_paused = not self.leve_paused
        
        #Navigate through the pause menu

        if(self.leve_paused):
              if(event.type == pygame.KEYUP):
                if(event.key == pygame.K_UP):
                    self.pause_menu_index -= 1
                    if(self.pause_menu_index < 0): self.pause_menu_index = 2
                elif(event.key == pygame.K_DOWN):
                    self.pause_menu_index += 1
                    if(self.pause_menu_index > 2): self.pause_menu_index = 0
                
                #Choosing pause menu options
                if(event.key == pygame.KSCAN_KP_ENTER or event.key == pygame.K_KP_ENTER):

                    match(self.pause_menu_index):

                        case 0:
                            self.leve_paused = False
                        case 1:
                            self.state_manager.set_state(Play(self.state_manager, self.level))
                        case 2:
                            self.state_manager.set_state(menu.Menu(self.state_manager))
         
#update logic for the game      
    def update(self):
    
        if(not( self.leve_cleared) and not(self.is_game_over) and not(self.leve_paused)):

            self.player.update()
            self.processTime()
        
            for crate in self.crates:
                crate.update()

            for brick in self.bricks:
                brick.update()

            for tile in self.dest_tiles:
                tile.update()

            self.check_collision_with_brick()
            self.check_x_marked_tiles()

#render all the entities in the game
    def render(self, surf):
        self.draw_floor(surf)

        for tile in self.dest_tiles:
            tile.render(surf)
        self.player.render(surf)

        for crate in self.crates:
            crate.render(surf)

        for brick in self.bricks:
            brick.render(surf)

        self.draw_HUD(surf)

        #Show the level clear menu
        if(self.leve_cleared):
            self.show_win_menu(surf)

        #Show the game over menu
        if(self.is_game_over):
            self.show_game_over(surf)
        #Show the level puased menu
        if(self.leve_paused):
            self.show_pause_menu(surf)

#handle collsion for the entities
    def check_collision_with_brick(self):

        #move the crate
    
        for crate in self.crates:
            if(self.player.rect.colliderect(crate.rect)):
                
                if(self.player.direction == Player.UP):
                    if(crate.y > 0 and not(crate.state == Crate.UP)):
                        crate.y -= crate.step_size
                        crate.direction = Crate.UP
                    

                    if(crate.state == Crate.UP):self.player.y = crate.y + 32
                    
                elif(self.player.direction == Player.DOWN):
                    if(crate.y < HEIGHT - 32 and not(crate.state == Crate.DOWN)):
                        crate.y += crate.step_size
                        crate.direction = Crate.DOWN
                        
                    if(crate.state == Crate.DOWN):self.player.y = crate.y - 32

                elif(self.player.direction == Player.RIGHT):
                    if(crate.x < WIDTH - 32 and not(crate.state == Crate.RIGHT)):
                        crate.x += crate.step_size
                        crate.direction = Crate.RIGHT
                        

                    if(crate.state == Crate.RIGHT):self.player.x -= crate.step_size 

                else:
                    if(crate.x > 0 and not(crate.state == Crate.LEFT)):
                        crate.x -= crate.step_size
                        crate.direction = Crate.LEFT 
                        

                    if(crate.state == Crate.LEFT):self.player.x = crate.x + 32

        #Check collision between crate and walls
        for brick in self.bricks:
        
            for crate in self.crates:

                if(brick.rect.colliderect(crate.rect)):
                    if(crate.direction == Crate.RIGHT):
                        crate.x = brick.x - 32
                        crate.state = Crate.RIGHT
                        self.player.x = crate.x - 32
                    

                    elif(crate.direction == Crate.LEFT):
                        crate.x = brick.x + 32
                        crate.state = Crate.LEFT
                        self.player.x = crate.x + 32

                    elif(crate.direction == Crate.UP):
                        crate.y = brick.y + 32
                        crate.state = Crate.UP
                        self.player.y = crate.y + 32

                    elif(crate.direction == Crate.DOWN):
                        crate.y = brick.y - 32
                        crate.state = Crate.DOWN
                        self.player.y = crate.y - 32
                else:
                    crate.state = 0

                #Check collision between the player and the bricks

                if(brick.rect.colliderect(self.player.rect)):
                    if(self.player.direction == Player.LEFT):
                        self.player.x = brick.x + 32
                    elif(self.player.direction == Player.RIGHT):
                        self.player.x = brick.x - 32
                    elif(self.player.direction == Player.UP):
                        self.player.y =  brick.y + 32
                    else:
                        self.player.y = brick.y - 32
               

        
#load levels  
    def load_level(self, level):
        file = open(os.path.join('Levels', f'Level_{level}.txt'))
        lines = file.readlines()
       
        y = 0
        for line in lines:
            x = 0
            text = line
            for char in text:

                #Load the bricks
                if(char == "B"):
                    brick = Brick(x * 32, y * 32, 32, 32)
                    self.bricks.append(brick)

                #Load the pkayer
                if(char == "P"):
                    self.player = Player(x *32, y * 32,  32, 32)

                #Load the crates
                if(char == "C"):
                    crate = Crate(x * 32, y * 32, 32, 32)
                    self.crates.append(crate)

                if(char == "X"):
                    dest_tile = Dest_Tile(x *  32, y * 32)
                    self.dest_tiles.append(dest_tile)
                    self.count += 1
        
                x += 1

            y += 1

#Draw the floor
    def draw_floor(self, surf):

        
        for y in range(int(HEIGHT/32)):
            for x in range(int((WIDTH - 128)/32)):
                surf.blit(floor_tile_texture, (x * 32, y * 32), 
                pygame.Rect(0, 0, 32, 32))

#Draw Heads Up Display
    def draw_HUD(self, surf):

        #Draw the border
        hud = pygame.transform.scale(border_texture, (WIDTH-384, HEIGHT))
        surf.blit(hud, (384, 0))

        time_text_render = font.render(" TIME", 1, (255, 255, 255))
        level_text_render = font.render("LEVEL", 1, (255, 255, 255))
        level_text = font.render(f"     {self.level}    ", 1, (255, 255, 255))
        pause_text = font_2.render("ESC to pause", 1, (255, 255, 0))

        if(self.second >= 10):
            time_text = font.render(f"  0{self.minutes}:{self.second}",1,  (255, 255, 255))
        else:
            time_text = font.render(f"  0{self.minutes}:0{self.second}",1,  (255, 255, 255))

        text_x = 384
        surf.blit(time_text_render, (text_x + time_text_render.get_width()/2, 32))
        surf.blit(time_text, (text_x + time_text_render.get_width()/2, 80))
        surf.blit(level_text_render, ((text_x) + level_text_render.get_width()/2, 128 ))
        surf.blit(level_text, ((text_x) + level_text_render.get_width()/2, 128 + 64))
        surf.blit(pause_text, (text_x  + level_text_render.get_width()/2 -23, 256))
  
#Check if the player wins

    def check_x_marked_tiles(self):
        arrangement_count = 0
        for tile in self.dest_tiles:
            for crate in self.crates:

                if(tile.rect.colliderect(crate.rect)):
                    arrangement_count += 1
                   
                    if(arrangement_count == self.count):
                        self.leve_cleared = True
                    
        arrangement_count = 0
#Display the pause menu

    def show_pause_menu(self, surf):
         #Draw overlay
        s = pygame.Surface((WIDTH,  HEIGHT))
        s.set_alpha(128)
        surf.blit(s, (0, 0))

        #Show when the game has been paused
        level_text = font_3.render(f"Puased", 1, (255, 255, 255))
        surf.blit(level_text, (WIDTH/ 2 - level_text.get_width()/2,HEIGHT/2 - 100))

        #Show the pause menu items
        items = ['Resume Game', 'Restart Level', 'Go to Menu']
        index = 0
        for item in items:

            item_text = font.render(item, 1, (255, 255, 0))
            surf.blit(item_text, (WIDTH/2 - item_text.get_width()/2,
                                  HEIGHT/2 + 25 +(index * 32)))
            index += 1
        
        selector_text = font.render(">", 1, (255, 255, 255))
        surf.blit(selector_text, (WIDTH/2 - 128 ,
                                HEIGHT/2 + 25 +(self.pause_menu_index * 32)))

#Process the time of e level
    def processTime(self):
        self.timer += 1

        if(self.timer >= 60):
            
            if(self.second > 0): self.second -= 1
            self.timer = 0
        if(self.second <= 0):
            if(self.minutes > 0): 
                if(self.minutes > 0):self.minutes -= 1
                self.second = 59

        if( self.minutes == 0 and self.second == 0):
            self.is_game_over = True

#Display when it's game over
    def show_game_over(self, surf):

        #Draw overlay
        s = pygame.Surface((WIDTH,  HEIGHT))
        s.set_alpha(128)
        surf.blit(s, (0, 0))

        #Display game over tex
        level_text = font_3.render(f"Game Over", 1, (255, 255, 255))
        surf.blit(level_text, (WIDTH/ 2 - level_text.get_width()/2,
                              HEIGHT/2 - 50))

        #Display the info text about moving to the next level
        level_text = font.render(f"Press space to go to the menu.", 1, (255, 255, 255))
        surf.blit(level_text, (WIDTH/ 2 - level_text.get_width()/2,HEIGHT/2 + 100))

#Display the win menu
    def show_win_menu(self, surf):

        #Draw overlay

        s = pygame.Surface((WIDTH,  HEIGHT))
        s.set_alpha(128)
        surf.blit(s, (0, 0))

        if(self.level < 10):
            #Display info text about the level, current level
            level_text = font.render(f"Level {self.level} cleared!", 1, (255, 255, 255))
            surf.blit(level_text, (WIDTH/ 2 - level_text.get_width()/2,
                                HEIGHT/2 - 50))

            #Display the info text about moving to the next level
            level_text = font.render(f"Press space to go to the next level.", 1, (255, 255, 255))
            surf.blit(level_text, (WIDTH/ 2 - level_text.get_width()/2,
                                HEIGHT/2 + 100))
        else:

             #Display info text about the level, current level
            level_text = font.render(f"You have completed the game", 1, (255, 255, 255))
            surf.blit(level_text, (WIDTH/ 2 - level_text.get_width()/2,
                                HEIGHT/2 - 50))

            #Display the info text about moving to the next level
            level_text = font.render(f"Press space to go to the menu.", 1, (255, 255, 255))
            surf.blit(level_text, (WIDTH/ 2 - level_text.get_width()/2,
                                HEIGHT/2 + 100))

