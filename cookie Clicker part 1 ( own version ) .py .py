import pygame

pygame.init()

screen=pygame.display.set_mode((500,500))
pygame.display.set_caption("Cookie Clicker")


text_font=pygame.font.Font(None,50)
title=text_font.render("Cookie Clicker",True,"black")
title_rect = title.get_rect(center=(screen.get_width()/2, 50))

running=True

clock=pygame.time.Clock()  
                  
while running:

    screen.fill('white')

    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    screen.blit(title,title_rect)
    # screen.blit(title,(130,15))  old version 

    pygame.display.flip()

    clock.tick(60)       

pygame.quit 