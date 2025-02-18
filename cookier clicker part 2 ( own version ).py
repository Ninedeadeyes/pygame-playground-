import pygame

class Game:
    def __init__(self):
        self.cookies=0
        self.cookie_per_click=1
        self.cookie_image = pygame.image.load('cookie.png').convert_alpha()  # Load the cookie image
        self.cookie_rect = self.cookie_image.get_rect(center=(250, 250))  # Posit
        self.clicked=False
    
    def click_button(self):
        self.mouse_pos=pygame.mouse.get_pos()
        if self.cookie_rect.collidepoint(self.mouse_pos):
            print("colliding")

        screen.blit(self.cookie_image, self.cookie_rect)

    def render(self):
        self.click_button()    

pygame.init()

screen=pygame.display.set_mode((500,500))
pygame.display.set_caption("Cookie Clicker")
text_font=pygame.font.Font(None,50)
title=text_font.render("Cookie Clicker",True,"black")

game=Game()

running=True

clock=pygame.time.Clock()  
                  
while running:

    screen.fill('white')

    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False


    screen.blit(title,(130,15))

    game.render()
    pygame.display.flip()

    clock.tick(60)       

pygame.quit 