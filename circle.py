import pygame as pg
import random
import numpy as np
import math

# pygame setup
pg.init()


WIDTH, HEIGHT = 800,600 # screen size
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Circle") # title
clock = pg.time.Clock()
running = True
dt = 0

player_pos = pg.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    for event in pg.event.get():
        # pygame.QUIT event means X clicked
        if event.type == pg.QUIT:
            running = False
            
    # fill screen with color
    screen.fill("black")
    
    # Render here
    pg.draw.circle(screen, "red", player_pos, 40)

    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        player_pos.y -= 300 * dt
    if keys[pg.K_s]:
        player_pos.y += 300 * dt
    if keys[pg.K_a]:
        player_pos.x -= 300 * dt
    if keys[pg.K_d]:
        player_pos.x += 300 * dt   
    # flip() display to show on screen
    pg.display.flip()
    
    dt = clock.tick(60) / 1000 # limit fps to 60
    
pg.quit()