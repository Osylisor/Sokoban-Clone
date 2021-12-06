import pygame
from StateManager import Stage_Manger
from pygame.time import Clock
import menu


pygame.init()
pygame.font.init()



WIDTH, HEIGHT = 512  , 288 
scale_x, scale_y, = WIDTH, HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
render_target = pygame.Surface((scale_x, scale_y))
pygame.display.set_caption("SOKUBAN CLONE")
state_manager = Stage_Manger()
current_level = 1


#Initialize the game
def init_game():
    state_manager.set_state(menu.Menu(state_manager))
    


#Update the game
def update():
    state_manager.update()


#render everything on the screen
def render():

    global render_target
    
    
    render_target.fill((0, 0, 0), (0, 0, scale_x, scale_y))
    state_manager.render(render_target)
    screen.blit(render_target, (0, 0))
    pygame.display.update()
    


#Main Game
def main():
    global screen, render_target, scale_x, scale_y
    is_running = True
    init_game()
    clock = Clock()
    while(is_running):
        clock.tick(60)
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                is_running = False

            if(event.type ==pygame.VIDEORESIZE):
               
               render_target = pygame.transform.scale(render_target, (event.w,  event.h))
            
            state_manager.processInput(event)

        update()
        render()
    

#run the app

if(__name__ == "__main__"):
    main()