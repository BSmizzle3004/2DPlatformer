import pygame
import sys
import sys

sys.path.insert(0, '/Users/bensmith/Programming/NEA/2D Platformer/Main Game')
class Button():
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

def main():
    pygame.init()

    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 700

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Menu")

    new_game_img = pygame.image.load("../Images/new_game_image.png").convert_alpha()
    new_game_w, new_game_h = 250, 75
    new_game_img = pygame.transform.scale(new_game_img, (new_game_w, new_game_h))

    exit_game_img = pygame.image.load("../Images/exit_game_image.png").convert_alpha()
    exit_game_w, exit_game_h = 250, 75
    exit_game_img = pygame.transform.scale(exit_game_img, (exit_game_w, exit_game_h))

    resume_game_img = pygame.image.load("../Images/resume_game.png").convert_alpha()
    resume_game_w, resume_game_h = 250, 75
    resume_game_img = pygame.transform.scale(resume_game_img, (resume_game_w, resume_game_h))

    start_button = Button(screen, (WINDOW_WIDTH // 2) - (new_game_w // 2), (WINDOW_HEIGHT // 3.5) - (new_game_h // 2), new_game_img)
    resume_button = Button(screen, (WINDOW_WIDTH // 2) - (resume_game_w // 2), (WINDOW_HEIGHT // 2) - (resume_game_h // 1.5), resume_game_img)
    quit_button = Button(screen, (WINDOW_WIDTH // 2) - (exit_game_w // 2), (WINDOW_HEIGHT // 1.5) - (exit_game_h // 2), exit_game_img)

    running = True
    while running:
        screen.fill((85,206,255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if start_button.click():
            print("new game")

        if resume_button.click():
            print("RESUME GAME")
        if quit_button.click():
            pygame.quit()
            sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    main()
