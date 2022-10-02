
import path_generation
import pygame

pygame.init()
pygame.font.get_init()
mainClock = pygame.time.Clock()

black = (0,0,0)
white = (255,255,255)

window_size = (800,800)

window = pygame.display.set_mode((window_size[0], window_size[1]))
window.fill(white)

while True:
    window.fill(white)
    pattern = path_generation.generate_path()
    c = [0,0,0]
    for i in range(len(pattern)):
        pygame.draw.rect(window,c,(pattern[i][0]*window_size[0]/8,pattern[i][1]*window_size[0]/8,window_size[0]/8,window_size[0]/8))
        if c[0] != 240:
            c[0] += 10
        elif c[1] != 240:
            c[1] += 10
        else:
            c[2] += 10

    pygame.display.update()
    done = False
    while done == False:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                done = True

