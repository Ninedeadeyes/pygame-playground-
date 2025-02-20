import pygame

pygame.init()

screen=pygame.display.set_mode((500,500))
pygame.display.set_caption("Cookie Clicker")


text_font=pygame.font.Font(None,50)
title=text_font.render("Cookie Clicker",True,"black")

running=True

clock=pygame.time.Clock()  
                  
while running:

    screen.fill('white')

    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False


    screen.blit(title,(130,15))

    pygame.display.flip()

    clock.tick(60)       

pygame.quit 