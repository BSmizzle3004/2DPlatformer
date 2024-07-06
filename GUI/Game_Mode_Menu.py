import pygame
import sys
class Game_Mode_Menu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True

        single_player_img = pygame.image.load("../Images/cloud_img.png")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

    def draw(self):
        self.screen.fill((85, 206, 255))

    def run(self):
        while self.running:
            self.handle_events()
            clicked = self.draw()
            if clicked:
                return clicked