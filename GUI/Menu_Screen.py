import pygame
import sys
from Components import Button


class Menu_Screen:
    def __init__(self, screen):
        self.screen = screen
        self.running = True

        # Load images for buttons
        new_game_img = pygame.image.load("../Images/new_game_image.png").convert_alpha()
        new_game_w, new_game_h = 250, 75
        new_game_img = pygame.transform.scale(new_game_img, (new_game_w, new_game_h))

        exit_game_img = pygame.image.load("../Images/exit_game_image.png").convert_alpha()
        exit_game_w, exit_game_h = 250, 75
        exit_game_img = pygame.transform.scale(exit_game_img, (exit_game_w, exit_game_h))

        resume_game_img = pygame.image.load("../Images/resume_game.png").convert_alpha()
        resume_game_w, resume_game_h = 250, 75
        resume_game_img = pygame.transform.scale(resume_game_img, (resume_game_w, resume_game_h))

        self.start_button = Button(screen, (screen.get_width() // 2) - (new_game_w // 2), (screen.get_height() // 3.5) - (new_game_h // 2), new_game_img)
        self.resume_button = Button(screen, (screen.get_width() // 2) - (resume_game_w // 2), (screen.get_height() // 2) - (resume_game_h // 1.5), resume_game_img)
        self.quit_button = Button(screen, (screen.get_width() // 2) - (exit_game_w // 2), (screen.get_height() // 1.5) - (exit_game_h // 2), exit_game_img)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

    def draw(self):
        self.screen.fill((85, 206, 255))

        if self.start_button.click():
            return "game_mode_menu"
        if self.resume_button.click():
            return "resume_game"
        if self.quit_button.click():
            pygame.quit()
            sys.exit()

        pygame.display.update()

    def run(self):
        while self.running:
            self.handle_events()
            clicked = self.draw()
            if clicked:
                return clicked