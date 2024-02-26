import pygame

pygame.init()

pygame.display.set_caption("BLACKJACK🃏")
screen = pygame.display.set_mode((1600, 900))

fps = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    pygame.display.update()
    fps.tick(60)
