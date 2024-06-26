import pygame as pg
import random
import numpy as np
import math

# pygame setup
pg.init()


WIDTH, HEIGHT = 1024, 800 # screen size
screen = pg.display.set_mode((WIDTH, HEIGHT)) # initializes screen with specified dimensions
pg.display.set_caption("Sand Simulator") # sets window title
WHITE = (255, 255, 255) # sets white color
SAND = (194, 178, 128) # sets sand color
T = 8 # sets size of particles

class Grid: # defines "Grid" class
    def __init__(self): # defines constructor method for "Grid" class
        self.grid = np.zeros((WIDTH*2,HEIGHT+T)) # initializes instance variable "grid" as NumPy array of zeroes
        self.position = [] # initializes instance variable "position" as empty list
        
    def addSand(self, pointX, pointY): # defines method "addSand" that takes three parameters: self, pointX, and pointY
        if pointX >= 0 and pointX <= WIDTH and pointY >= 0 and pointY <= HEIGHT: # checks for valid coordinates
            if self.grid[pointX][pointY] == 0: # checks if grid cell is emply
                self.grid[pointX][pointY] = 1 # adds sand particle
                self.position.append((pointX, pointY)) #records coordinates to "position" list
    
    def update_position(self): # defines "update_position" method to to update positions of sand particles in self.position
        for points in self.position: # iterates over all positions in self.position
            listpoints = list(points) # converts tuple to a list
            self.position.remove(points) # current position is removes to update its new position later
            
            if points[1] >= HEIGHT - T: # if y coordinate of point is >= HEIGHT - T (at bottom of grid), point is re-added to self.position
                self.position.append(points)
                
            elif self.grid[points[0]][points[1]+T] == 0: # checks if cell blow is empty
                self.grid[points[0]][points[1]] = 0 # current cell is set to 0
                self.grid[points[0]][points[1]+T] = 1 # cell below is set to 1
                listpoints[1] += T # moves the y-coordinate of the particle down T units
                points = tuple(listpoints) # converts list back to a tuple
                self.position.append(points) # updated position tuple "points" is appended to self.position
            
            elif self.grid[points[0]][points[1]+T] == 1: # checks if cell below is occupied
                if (self.grid[points[0]+T][points[1]+T] == 1) and (self.grid[points[0]-T][points[1]+T] == 1): # checks if both bottom-right and bottom-left are occupied
                    self.position.append(points) # particle remains at current position
                    
                elif (self.grid[points[0]+T][points[1]+T] == 1) and (self.grid[points[0]-T][points[1]+T] == 0): # checks if bottom-right is occupied and bottom-left is empty
                    self.grid[points[0]][points[1]] = 0 # current cell is set to 0
                    self.grid[points[0]-T][points[1]+T] = 1 # the particle is moved down and left
                    listpoints[0] -= T # moves the x-coordinate of the particle left T units
                    listpoints[1] += T # moves the y-coordinate of the particle down T units
                    points = tuple(listpoints) # converts list back to a tuple
                    self.position.append(points) # updated position tuple "points" is appended to self.position
                
                elif (self.grid[points[0]+T][points[1]+T] == 0) and (self.grid[points[0]-T][points[1]+T] == 1): # checks if bottom-left is occupied and bottom-right is empty
                    self.grid[points[0]][points[1]] = 0 # current cell is set to 0
                    self.grid[points[0]+T][points[1]+T] = 1 # the particle is moved down and right 
                    listpoints[0] += T # moves the x-coordinate of the particle left T units
                    listpoints[1] += T # moves the y-coordinate of the particle down T units
                    points = tuple(listpoints) # converst list back to a tuple
                    self.position.append(points) # updated position tuple "points" is appended to self.position

                else:
                    self.grid[points[0]][points[1]] = 0 # checks if  ottom-left and bottom-right cells are both empty
                    a = random.randint(0,1) # generate random 0 or 1
                    if a == 0: # if a is 0, changes a to -1
                        a = -1
                    self.grid[points[0]+a*T][points[1] + T] = 1 # changes particle to bottom-left or -right as a result of random 0 or 1
                    listpoints[0] += a*T # moves the x-coordiate of the particle left or right T units
                    listpoints[1] += T # moves the y-coordinate of the particle down T units
                    points = tuple(listpoints)
                    self.position.append(points)

                
    def draw(self, screen): # defines draw function: self (refers to the instnace of Grid class) and screen (the pygame screen)
        for points in self.position: # iterates over each point in self.position as a list that contains the coordiantes of all sand particles present in grid
            pg.draw.rect(screen, SAND, (points[0], points[1], T, T), 0) # pygame function that draws rectangle on screen
            # screen is surface that rectangle is drawn on
            # SAND is color of rectangle defined earlier
            # (points[0], points[1], T, T) specifies position and size of rectangle
                # points[0] is x-coordinate of top left corner of rectangle
                # points [1] is y-coordinate of top left corner of rectangle
                # T is width of rectangle
                # T is also height of rectangle
            # 0 specifies that the rectablge should be filled in

def main():
    running = True # boolian variable that controls main game loop
    clock = pg.time.Clock() # Pygame object to manage frame rate
    
    sandbox = Grid() # sets instance of Grid class
    
    while running: # while loop to run game
        clock.tick(60) # limit fps to 60
        pg.display.set_caption("Falling Sand - FPS: {}".format(int(clock.get_fps()))) # display caption including current fps
        screen.fill("black") # fill screen with color

        # poll for events
        for event in pg.event.get():
            # pygame.QUIT event means X clicked
            if event.type == pg.QUIT:
                running = False
                
            elif pg.mouse.get_pressed()[0]: # if left mouse button is pressed
                pos=pg.mouse.get_pos() # mouse position obtained
                sandbox.addSand(pos[0]-pos[0]%T, pos[1]-pos[1]%T) # adds sand at mouse position on grid, adjusted to alight with grid cell size T
                
        
        # Render here
        sandbox.update_position() # updates positions of all sand particles on grid
        sandbox.draw(screen) # draws the updated positions of sand particles on screed
        
        pg.display.update() # updates the display with new frame, rending drawn particles
        
    pg.quit() 

main()