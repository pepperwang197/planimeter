from time import sleep
import pygame
from arms import Arm

scrn = pygame.display.set_mode((600, 600))
pygame.display.set_caption("image")

prev_xy = (0, 0)
xy = (0, 0)

all_coords = []

while True:
    pygame.event.get()
    if pygame.mouse.get_pressed()[0]:
        xy = pygame.mouse.get_pos()
        if prev_xy != (0, 0):
            pygame.draw.line(scrn, "white", prev_xy, xy)
        all_coords.append(xy)
        prev_xy = xy
        print(xy)

    pygame.display.flip()
    sleep(0.02)
