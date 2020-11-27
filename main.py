import pygame
from Square import Square
from AStarPathfinding import pathfind
pygame.init()

#CONSTANTS: These affect how the program runs
#Heuristics constant that determines nature of pathfinding
h_const = 1
#square size in pixels
square_size = 10
#number of squares on screen
num_squares = (50,50)

def main():
    """Set up the GUI, initalise the squares matrix, handle events"""
    #set a title
    pygame.display.set_caption("Path Finding")
    board_dimensions = (square_size*num_squares[0], square_size*num_squares[1])
    board = pygame.Rect(0,0,board_dimensions[0],board_dimensions[1])
    #Define the dimensions for the control section of the board
    control_dimensions = (board_dimensions[0], 50)
    control = pygame.Rect(0,board_dimensions[1],control_dimensions[0],control_dimensions[1])
    #Set the screen itself by combining the board and control sections
    screen = pygame.display.set_mode((board_dimensions[0],board_dimensions[1]+control_dimensions[1]))
    pygame.draw.rect(screen, pygame.Color(128,128,128), control)
    
    #set the buttons up
    BUTTON_FONT = pygame.font.Font(None, 32)
    BUTTON_FONT_COLOR = pygame.Color(0,0,0)
    #start button
    start_button = pygame.Rect(control.x+control.width//8,
                               control.y+control.height//10,
                               2*control.width//8,
                               8*control.height//10)
    pygame.draw.rect(screen, pygame.Color(200,200,200), start_button)
    screen.blit(BUTTON_FONT.render("START", True, BUTTON_FONT_COLOR),
                (start_button.x+2*start_button.width//10,
                 start_button.y+3*start_button.height//10))
    #state (wall/empty) button
    state_button_state = Square.STATE.WALL
    state_button = pygame.Rect(control.x+5*control.width//8,
                               control.y+control.height//10,
                               2*control.width//8,
                               8*control.height//10)
    pygame.draw.rect(screen, pygame.Color(200,200,200), state_button)
    screen.blit(BUTTON_FONT.render(state_button_state.name, True, BUTTON_FONT_COLOR),
                (state_button.x+2.25*state_button.width//10,
                 state_button.y+3*state_button.height//10))

    #initalise each square into a 2d matrix
    squares = list()
    for x in range(num_squares[0]):
        squares.append([])
        for y in range(num_squares[1]):
            squares[x].append(Square((x*square_size,y*square_size), square_size))
            squares[x][y].draw(screen)
    #We set the upper left square to the source
    squares[0][0].set_state(Square.STATE.SOURCE)
    squares[0][0].draw(screen)
    #And the lower right square to the target
    squares[-1][-1].set_state(Square.STATE.TARGET)
    squares[-1][-1].draw(screen)

    #Update the screen to show the buttons and squares
    pygame.display.update()
    
    # main loop
    running = True
    #Flag to track when the mouse is down, for drawing walls etc
    mouse_down_flag = False
    #Flag to track when the algorithm is ready to run
    #This just stops the user from drawing walls onto a running/completed simulation
    ready_flag = True
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            #If exit button is clicked, exit the game
            if event.type == pygame.QUIT:
                return squares
                running=False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not ready_flag and not start_button.collidepoint(event.pos):
                    #Eat all inputs that are not clicking reset when reset needed
                    continue
                mouse_down_flag = True
                #Check if a button was clicked
                if start_button.collidepoint(event.pos):
                    #If the board needs to be reset, reset it
                    if not ready_flag:
                        #Redraw the start button
                        pygame.draw.rect(screen, pygame.Color(200,200,200), start_button)
                        screen.blit(BUTTON_FONT.render("START", True, BUTTON_FONT_COLOR),
                                (start_button.x+2*start_button.width//10,
                                 start_button.y+3*start_button.height//10))
                        #Reset the squares all to empty
                        squares = list()
                        for x in range(num_squares[0]):
                            squares.append([])
                            for y in range(num_squares[1]):
                                squares[x].append(Square((x*square_size,y*square_size), square_size))
                                squares[x][y].draw(screen)
                        #Reset the target and source squares
                        squares[0][0].set_state(Square.STATE.SOURCE)
                        squares[0][0].draw(screen)
                        squares[-1][-1].set_state(Square.STATE.TARGET)
                        squares[-1][-1].draw(screen)
                        #Update the GUI with all the resets
                        pygame.display.update()
                        ready_flag = True
                    #If the board IS ready, run the pathfinding
                    else:
                        #Get the path determined
                        path = pathfind(screen, squares)
                        #If the path wasn't complete, it is None so it's false-y
                        if path:
                            #Draw the path to the GUI
                            for pos in path:
                                squares[pos[0]][pos[1]].set_state(Square.STATE.PATH)
                                squares[pos[0]][pos[1]].draw(screen)
                        #Draw the start button as the reset button
                        pygame.draw.rect(screen, pygame.Color(200,200,200), start_button)
                        screen.blit(BUTTON_FONT.render("RESET", True, BUTTON_FONT_COLOR),
                                    (start_button.x+2*start_button.width//10,
                                     start_button.y+3*start_button.height//10))
                        ready_flag = False
                    #Force the flag to be False, so the user cannot draw walls
                    mouse_down_flag = False
                #If user clicks on state button
                if state_button.collidepoint(event.pos):
                    #Change the state to draw, then update the button
                    state_button_state = Square.STATE.WALL if state_button_state==Square.STATE.EMPTY else Square.STATE.EMPTY
                    pygame.draw.rect(screen, pygame.Color(200,200,200), state_button)
                    screen.blit(BUTTON_FONT.render(state_button_state.name, True, BUTTON_FONT_COLOR),
                                (state_button.x+2.25*state_button.width//10,
                                 state_button.y+3*state_button.height//10))
                    mouse_down_flag = False

            #If the user mouseups, change the flag
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_down_flag = False
            #if the mouse button is being held down, check if the mouse passes through a square
            if mouse_down_flag:
                mouse_pos = pygame.mouse.get_pos()
                #Loop through every square and check if it has collided
                #There MUST be a best way to do this, I think using mouse_pos to find the index we want...
                #This is still pretty darn quick
                for x in range(num_squares[0]):
                    for y in range(num_squares[1]):
                        if squares[x][y].rect.collidepoint(mouse_pos):
                            #Set the state to what is determined by the state button
                            squares[x][y].set_state(state_button_state)
                            #Reset the source and target, just in case they get drawn over
                            squares[0][0].set_state(Square.STATE.SOURCE)
                            squares[-1][-1].set_state(Square.STATE.TARGET)
                            squares[x][y].draw(screen)
        #Update the screen                    
        pygame.display.update()

if __name__ == "__main__":
    main()
    pygame.quit()
    

