import pygame
import sys
import socket
import threading
import json
import time

HOST = "127.0.0.1"
PORT = 50000

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
BLOCK_SIZE = 45
block_array = []

# Reading block positions from text file
with open("../Map Builder/block_positions.txt", "r") as file:
    for line in file:
        block_array.append(line.strip().split())

pygame.display.init()
pygame.font.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)

fire_img_1 = pygame.image.load("../Images/fire_block_1.png").convert_alpha()
scaled_block_image = pygame.transform.scale(fire_img_1, (BLOCK_SIZE, BLOCK_SIZE))

players = pygame.sprite.Group()


# Receiving data from the server
def recv_from_server(connection, game):
    while True:
        data = connection.recv(4096)
        if not data:
            break
        else:
            data = data.decode()
            packet = json.loads(data)

            if packet["command"] == "MOVE":
                other = players.sprites()[1]
                other.x = packet["position"][0]
                other.y = packet["position"][1]
                other.set_direction(packet["facing_right"])
            elif packet["command"] == "SETUP":
                global block_array
                block_array = packet["map"]
                other_position = packet["position2"]
                my_position = packet["position1"]
                main = Player(my_position[0], my_position[1], game=game, client=connection)
                players.add(main)
                game.set_player(main)
                other = Player(other_position[0], other_position[1], game=game, client=connection)
                players.add(other)
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

class Character:
    def __init__(self, x, y, health, speed):
        self.x = x
        self.y = y
        self.health = health
        self.speed = speed

    def draw(self, screen, image):
        screen.blit(image, (self.x, self.y))
class Player(pygame.sprite.Sprite, Character):
    def __init__(self, x, y, health=100, speed=7, game=None, client=None):
        Character.__init__(self, x, y, health, speed)
        pygame.sprite.Sprite.__init__(self)

        self.__player_right_img = pygame.image.load("../Images/player_right_img.png").convert_alpha()
        self.__scaled_player_right_image = pygame.transform.scale(self.__player_right_img, (int(self.__player_right_img.get_width() * 0.18), int(self.__player_right_img.get_height() * 0.18)))
        self.__player_left_img = pygame.image.load("../Images/player_left_img.png").convert_alpha()
        self.__scaled_player_left_image = pygame.transform.scale(self.__player_left_img, (int(self.__player_left_img.get_width() * 0.18), int(self.__player_left_img.get_height() * 0.18)))
        self.image = self.__scaled_player_right_image
        self.__game = game

        self.__vertical_speed = 0
        self.rect = pygame.Rect(x, y, self.__scaled_player_right_image.get_width(), self.__scaled_player_right_image.get_height())
        self.__is_on_ground = False
        self.__facing_right = True
        self.__client = client

    def move(self, block_rects, level_width):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        # Movement handling
        if keys[pygame.K_d]:
            dx += self.speed
            self.__facing_right = True
            self.tell_server()

        if keys[pygame.K_a]:
            dx -= self.speed
            self.__facing_right = False
            self.tell_server()

        if keys[pygame.K_SPACE] and self.__is_on_ground:
            self.__vertical_speed = -8
            self.__is_on_ground = False
            self.tell_server()

        self.__vertical_speed += 0.3
        dy += self.__vertical_speed

        self.__is_on_ground = False

        grid_pos_x = self.rect.x // BLOCK_SIZE
        grid_pos_y = self.rect.y // BLOCK_SIZE

        neighbours = [
            (grid_pos_x - 1, grid_pos_y),
            (grid_pos_x + 1, grid_pos_y),
            (grid_pos_x, grid_pos_y - 1),
            (grid_pos_x, grid_pos_y + 1),
            (grid_pos_x - 1, grid_pos_y - 1),
            (grid_pos_x + 1, grid_pos_y + 1),
            (grid_pos_x - 1, grid_pos_y + 1),
            (grid_pos_x + 1, grid_pos_y - 1)
        ]

        camera_x, camera_y = self.__game.get_camera_offset()

        for nx, ny in neighbours:
            if 0 <= nx < WINDOW_WIDTH and 0 <= ny < WINDOW_HEIGHT:
                neighbour_rect = pygame.Rect(nx * BLOCK_SIZE - camera_x, ny * BLOCK_SIZE - camera_y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, (0, 255, 0), neighbour_rect, 2)

        neighbour_rects = []
        for nx, ny in neighbours:
            if 0 <= nx < len(block_array[0]) and 0 <= ny < len(block_array):
                if block_array[ny][nx] == "F":
                    neighbour_rects.append(pygame.Rect(nx * BLOCK_SIZE, ny * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        # Collision detection
        self.rect.x += dx
        for block in neighbour_rects:
            if self.rect.colliderect(block):
                if dx > 0:
                    self.rect.right = block.left
                if dx < 0:
                    self.rect.left = block.right

        self.rect.y += dy
        for block in neighbour_rects:
            if self.rect.colliderect(block):
                if dy > 0:
                    self.rect.bottom = block.top
                    self.__is_on_ground = True
                    self.__vertical_speed = 0
                if dy < 0:
                    self.rect.top = block.bottom
                    self.__vertical_speed = 0

        # Screen collisions
        if self.rect.x <= 0:
            self.rect.left = 0

        if self.rect.right >= level_width:
            self.rect.right = level_width

        self.x, self.y = self.rect.topleft

        if not self.__is_on_ground:
            self.tell_server()

    def attack(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            print("attack")

    def get_scaled_image(self):
        if self.__facing_right:
            return self.__scaled_player_right_image
        else:
            return self.__scaled_player_left_image

    def set_direction(self, facing_right):
        self.__facing_right = facing_right

    # Sending movement data to the server
    def tell_server(self):
        if self.__client is not None:
            packet = {
                "command": "MOVE",
                "position": [self.rect.x, self.rect.y],
                "facing_right": self.__facing_right,
            }
            self.__client.send(json.dumps(packet).encode())
            time.sleep(0.0005)

    def get_position(self):
        return self.x, self.y

    def draw(self, screen):
        image = self.get_scaled_image()
        camera_x, camera_y = self.__game.get_camera_offset()
        screen.blit(image, (self.x - camera_x, self.y - camera_y))

class Game:
    def __init__(self):
        self.__WINDOW_WIDTH = 1200
        self.__WINDOW_HEIGHT = 700
        self.__screen = pygame.display.set_mode((self.__WINDOW_WIDTH, self.__WINDOW_HEIGHT))
        self.__clock = pygame.time.Clock()
        self.__running = True
        self.__camera_x = 0
        self.__camera_y = 0
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.connect((HOST, PORT))
        self.level_width = len(block_array[0]) * BLOCK_SIZE
        self.__player = None

        # Server communication threading
        threading.Thread(target=recv_from_server, args=(self.__client, self)).start()
        while self.__player is None:
            self.__screen.fill((255, 255, 255))
            my_font = pygame.font.SysFont('Comic Sans MS', 30)
            text_surface = my_font.render('Waiting for 2nd Player', False, (0, 0, 0))
            self.__screen.blit(text_surface, (self.__WINDOW_WIDTH // 2 - text_surface.get_width() // 2, self.__WINDOW_HEIGHT // 2 - text_surface.get_height() // 2))
            pygame.display.flip()

    def set_player(self, player):
        self.__player = player

    def run_game(self):
        while self.__running:
            self.handle_events()
            self.update()
            self.render()
            self.__clock.tick(60)
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False

    # Updates player movement and collisions
    def update(self):
        self.__screen.fill((75, 75, 75))
        block_rects = []
        for y, row in enumerate(block_array):
            for x, val in enumerate(row):
                if val == "F":
                    block_rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    block_rects.append(block_rect)

        self.__player.move(block_rects, self.level_width)
        players.update()

    # Renders the game world
    def render(self):
        camera_x, camera_y = self.get_camera_offset()

        for y, row in enumerate(block_array):
            for x, val in enumerate(row):
                if val == "F":
                    block_rect = pygame.Rect(x * BLOCK_SIZE - camera_x, y * BLOCK_SIZE - camera_y, BLOCK_SIZE, BLOCK_SIZE)
                    self.__screen.blit(scaled_block_image, block_rect)
                if val == "E":
                    red_square_rect = pygame.Rect(x * BLOCK_SIZE - camera_x, y * BLOCK_SIZE - camera_y, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(self.__screen, (255, 0, 0), red_square_rect)

        for player in players.sprites():
            player.draw(self.__screen)
        pygame.display.update()

    def get_camera_offset(self):
        player_x, player_y = self.__player.get_position()
        camera_x = player_x - self.__WINDOW_WIDTH // 2
        camera_y = player_y - self.__WINDOW_HEIGHT // 2
        return camera_x, camera_y

if __name__ == "__main__":
    menu = Menu_Screen(screen)

    if menu.run() == "new_game":
        game_mode = Game_Mode_Menu(screen)
        if game_mode.run() == ""

    else:
        pygame.quit()
        sys.exit()
