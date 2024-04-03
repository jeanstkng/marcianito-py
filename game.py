import pygame

pygame.init()
window = pygame.display.set_mode((640,480))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    
    pygame.draw.rect(window, (0,0,255), (120,120,400,240))
    pygame.display.update()

pygame.quit()