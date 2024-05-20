import pygame as pg
import random
import numpy as np
import math

# pygame setup
pg.init()


WIDTH, HEIGHT = 1024, 800 # screen size
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Sand Simulator") # title
WHITE = (255, 255, 255)
SAND = (194, 178, 128)
T = 8

class Grid:
    def __init__(self):
        self.grid = np.zeros((WIDTH*2,HEIGHT+T))
        self.position = []
        
    def addSand(self, pointX, pointY):
        if pointX >= 0 and pointX <= WIDTH and pointY >= 0 and pointY <= HEIGHT:
            if self.grid[pointX][pointY] == 0:
                self.grid[pointX][pointY] = 1
                self.position.append((pointX, pointY))
    
    def update_position(self):
        for points in self.position:
            listpoints = list(points)
            self.position.remove(points)
            
            if points[1] >= HEIGHT-T:
                self.position.append(points)
                
            elif self.grid[points[0]][points[1]+T] == 0:
                self.grid[points[0]][points[1]] = 0
                self.grid[points[0]][points[1]+T] = 1 
                listpoints[1] += T
                points = tuple(listpoints)
                self.position.append(points)
                
    def draw(self, screen):
        for points in self.position:
            pg.draw.rect(screen, SAND, (points[0], points[1], T, T), 0)


def main():
    running = True
    clock = pg.time.Clock()
    
    sandbox = Grid()
    
    while running:
        clock.tick(60) # limit fps to 60
        pg.display.set_caption("Falling Sand - FPS: {}".format(int(clock.get_fps()))) # display caption
        screen.fill("black") # fill screen with color

        # poll for events
        for event in pg.event.get():
            # pygame.QUIT event means X clicked
            if event.type == pg.QUIT:
                running = False
                
            elif pg.mouse.get_pressed()[0]:
                pos=pg.mouse.get_pos()
                button=pg.mouse
                sandbox.addSand(pos[0]-pos[0]%T, pos[1]-pos[1]%T)
                
        
        # Render here
        sandbox.update_position()
        sandbox.draw(screen)
        
        pg.display.update()
        
    pg.quit()

main()