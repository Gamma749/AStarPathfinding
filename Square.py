from enum import Enum
import pygame

class Square:
    """
    Class for each Square that fills the board

    Classes:
    -------------------
    STATE
        Enumerated type that denotes how the Square object should act

    Attributes:
    -------------------
    pos : (int, int)
        The position in pixels of the upperleft corner of the square on the board (x,y)

    size : int
        The length of the sides of the squares
        
    index : (int, int)
        The index of this square in the squares matrix. Functionally the same as pos

    COLOR : {STATE, pygame.Color}
        A dictionary that relates a Square.STATE to a Color
        It is this color that will be drawn onto the screen

    Methods:
    -------------------
    draw(screen)
        Draw the square onto the screen, using the color determined by the squares STATE

    set_state(Square.STATE)
        Set the state of this square, useful so the state is kept once a scope is left
    
    """
    class STATE(Enum):
        """
        An enumerated class that carries the state of a square
        """
        EMPTY=1
        OPEN=2
        CLOSED=3
        WALL=4
        SOURCE=5
        TARGET=6
        PATH=7
        
    COLOR={
        STATE.EMPTY:pygame.Color(255,255,255),
        STATE.OPEN:pygame.Color(50,50,200),
        STATE.CLOSED:pygame.Color(50,200,50),
        STATE.WALL:pygame.Color(0,0,0),
        STATE.SOURCE:pygame.Color(0,255,0),
        STATE.TARGET:pygame.Color(255,0,0),
        STATE.PATH:pygame.Color(255,0,255)
        }
    
    def __init__(self, pos, size):
        """
        Parameters:
        ----------------
        pos: (int, int)
            The pixel position to place the square (upperleft corner coordinate)

        size: int
            The side length of the square
        """
        self.rect = pygame.Rect(pos, (size,size))
        self.index = (pos[0]//size, pos[1]//size)
        self.state = Square.STATE.EMPTY

    def draw(self, screen):
        """
        Draw a square with a border onto the screen given

        Parameters:
        ----------------
        screen: pygame.surface
            The surface to draw the square onto
        """
        #Draw the border, which is just a black square beneath the square
        pygame.draw.rect(screen, Square.COLOR[Square.STATE.WALL], self.rect)
        #Draw the square itself
        inner_square = pygame.Rect(self.rect.x+1, self.rect.y+1,
                                   self.rect.width-1, self.rect.height-1)
        pygame.draw.rect(screen, Square.COLOR[self.state], inner_square)
        

    def set_state(self, state):
        """
        Set the state of the square

        Parameters:
        ----------------
        state: Square.STATE
            The state to be set
        """
        self.state=state
