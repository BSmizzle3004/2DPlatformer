import pygame


class Button:
    def __init__(self, screen, x, y, image):
        self.screen = screen
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def click(self):
        clicked = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                clicked = True

        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        return clicked
