import pygame
import sys
import sqlite3, hashlib
from datetime import datetime

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
BLOCK_SIZE = 50

GRID_WIDTH = WINDOW_WIDTH // BLOCK_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // BLOCK_SIZE

GREY = (75, 75, 75)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Map Builder")

clock = pygame.time.Clock()

image = pygame.image.load("/Users/bensmith/Programming/NEA/2D Platformer/Images/fire_block_1.png").convert()
image = pygame.transform.scale(image, (BLOCK_SIZE, BLOCK_SIZE))

rectangles = []
block_array = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

running = True

def runsql(*args):
    conn = sqlite3.connect("../Map Builder/User_Data.db")
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()
    if len(args) == 1:
        cursor.execute(args[0])
    else:
        cursor.execute(args[0], args[1])

    conn.commit()
    return cursor.fetchall()

def get_grid_position(x, y):
    grid_x = x // BLOCK_SIZE
    grid_y = y // BLOCK_SIZE
    return grid_x, grid_y

conn = sqlite3.connect('User_Data.db')
conn.execute("PRAGMA foreign_keys = 1")
c = conn.cursor()

def save_map(user_id, map_data):
    c.execute('INSERT INTO maps (user_id, map_data) VALUES (?, ?)', (user_id, map_data))
    conn.commit()

username = input("Username: ")
password = input("Password: ")
password_hash = hashlib.sha256(password.encode()).hexdigest()

user_query = "SELECT UserID FROM UserData WHERE Username = ? AND Password = ?"
user_result = c.execute(user_query, (username, password_hash)).fetchone()

if user_result:
    user_id = user_result[0]
    print("Login successful")
else:
    print("Login failed")
    pygame.quit()
    sys.exit()

while running:
    screen.fill(GREY)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_f]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x, grid_y = get_grid_position(mouse_x, mouse_y)
            new_rect = pygame.Rect(grid_x * BLOCK_SIZE, grid_y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            if block_array[grid_y][grid_x] == 0:
                rectangles.append(new_rect)
                block_array[grid_y][grid_x] = "F"

        if keys[pygame.K_r]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x, grid_y = get_grid_position(mouse_x, mouse_y)
            if block_array[grid_y][grid_x] == "F":
                for rect in rectangles:
                    if rect.x == grid_x * BLOCK_SIZE and rect.y == grid_y * BLOCK_SIZE:
                        rectangles.remove(rect)
                        block_array[grid_y][grid_x] = 0
                        break

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if block_array[y][x] == "F":
                screen.blit(image, (x * BLOCK_SIZE, y * BLOCK_SIZE))

    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, GREY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, GREY, (0, y), (WINDOW_WIDTH, y))

    pygame.display.flip()
    clock.tick(60)

map_data = "\n".join([" ".join(map(str, row)) for row in block_array])

save_map(user_id, map_data)

sql_delete = "DELETE FROM maps"
runsql(sql_delete)


for row in block_array:
    print(row)

pygame.quit()
conn.close()
sys.exit()
