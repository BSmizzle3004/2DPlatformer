import pygame, sys
from queue import PriorityQueue

pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
RED = (230, 9, 1)
GREEN = (2, 245, 0)
GREY = (75, 75, 75)
BLUE = (0, 0, 240)
PURPLE = (160, 32, 240)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 140, 0)
LIGHT_BLUE = (0, 255, 255)

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("A* Pathfinding Algorithm")

ROWS = 50
COLS = 50

CELL_SIZE = WINDOW_WIDTH / ROWS

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = None
        self.colour = GREY
        self.neighbours = []

    def set_colour(self, colour):
        self.colour = colour

    def get_pos(self):
        return self.row, self.col

    def A_Star_Algo(self, grid, end):
        self.neighbours = []
        if self.row < ROWS - 1 and not grid[self.row + 1][self.col].is_obstacle():
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_obstacle():
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < COLS - 1 and not grid[self.row][self.col + 1].is_obstacle():
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_obstacle():
            self.neighbours.append(grid[self.row][self.col - 1])

    def is_obstacle(self):
        return self.colour == BLACK

    def __lt__(self, other):
        return False

def algorithm(draw, grid, start, end):
    draw()
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = distance(start, end)

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[1]

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.set_colour(PURPLE)
            return True

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + distance(neighbour, end)
                if neighbour not in [node[1] for node in open_set.queue]:
                    open_set.put((f_score[neighbour], neighbour))
                    neighbour.set_colour(LIGHT_BLUE)

        draw()

        if current != start:
            current.set_colour(RED)

    return False

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.set_colour(ORANGE)
        draw() 

grid = []
for row in range(ROWS):
    grid.append([])
    for col in range(COLS):
        node = Node(row, col)
        grid[row].append(node)

def draw_node(SCREEN, grid):
    for row in grid:
        for node in row:
            pygame.draw.rect(SCREEN, node.colour, (node.col * CELL_SIZE, node.row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def handle_mouse_click(pos, grid, start, end):
    x, y = pos
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    node = grid[int(row)][int(col)]

    if pygame.mouse.get_pressed()[0]:
        if not start:
            start = node
            start.set_colour(RED)
        elif not end and node != start:
            end = node
            end.set_colour(GREEN)
        elif node != start and node != end:
            node.set_colour(BLACK)

    elif pygame.mouse.get_pressed()[2]:
        if node == start:
            start = None
        elif node == end:
            end = None
        node.set_colour(GREY)

    return start, end

def distance(node1, node2):
    return abs(node1.row - node2.row) + abs(node1.col - node2.col)

def clear_grid(grid):
    for row in grid:
        for node in row:
            node.set_colour(GREY)
    return None, None


def main():
    run = True
    start = None
    end = None

    while run:
        SCREEN.fill(GREY)
        draw_node(SCREEN, grid)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                start, end = handle_mouse_click(pos, grid, start, end)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.A_Star_Algo(grid, end)
                    algorithm(lambda: draw_node(SCREEN, grid), grid, start, end)

                if event.key == pygame.K_c:
                    start, end = clear_grid(grid)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
