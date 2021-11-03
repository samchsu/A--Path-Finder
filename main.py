from types import LambdaType
import pygame
from queue import PriorityQueue
import sys

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))

pygame.display.set_caption("A* Path-Finding Algorithm")
pygame.init() # now use display and fonts
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

DGRAY = (169, 169, 169)
BROWN = (89, 38, 11)
BLUE = (0, 0, 255)
YELLOW = (208, 135, 54)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CREME = (251, 219, 160)
ORANGE= (255, 165, 0)
GRAY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
 
class Square:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == DGRAY
    
    def is_open(self):
        return self.color == BROWN
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == CREME

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE
    
    def make_closed(self):
        self.color = DGRAY
    
    def make_open(self):
        self.color = BROWN
    
    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = CREME

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # go down
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # go up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # go right
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # go left
            self.neighbors.append(grid[self.row][self.col - 1])

    def __it__(self, other):
        return False

def h(p1, p2): # heuristic approach - manhattan distance
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from: 
        current = came_from[current]
        current.make_path()
        draw()

def algo(draw, grid, start, end): # f(n) = g(n) + h(n)
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start)) # add to priority queue
    came_from = {} #dict
    g_score = {square: float("inf") for row in grid for square in row} # starts at infinity
    g_score[start] = 0
    f_score = {square: float("inf") for row in grid for square in row} # starts at infinity 
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end: # found the shortest path 
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1 
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count+=1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()
    return False
    
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            square = Square(i, j, gap, rows)
            grid[i].append(square)
    return grid

def draw_grid(win, rows, width): # set the lines for grid
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GRAY, (0, i * gap), (width, i * gap))
        pygame.draw.line(win, GRAY, (i * gap, 0), (i * gap, width))

def draw(win, grid, rows, width): # set the blank palette
    win.fill(WHITE)
    for row in grid:
        for square in row:
            square.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col

def instruction(run, display_instructions, font, font1):
    while run and display_instructions:
        WIN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                display_instructions = False
        text = font1.render("A* Path-Finding Visualization", True, CREME)
        text_rect = text.get_rect(center=(WIDTH/2, (WIDTH/2)-100))
        WIN.blit(text, text_rect)

        text = font.render("1. Set the start and end points first, then draw barriers", True, CREME)
        text_rect2 = text.get_rect(center=((WIDTH/2), (WIDTH/2)))
        WIN.blit(text, text_rect2)

        text = font.render("2. Press SPACE to run and 'c' key to clear", True, CREME)
        text_rect2 = text.get_rect(center=((WIDTH/2), (WIDTH/2)+50))
        WIN.blit(text, text_rect2)

        text = font.render("3. Revisit this screen by pressing 'm' key", True, CREME)
        text_rect2 = text.get_rect(center=((WIDTH/2), (WIDTH/2)+100))
        WIN.blit(text, text_rect2)

        text = font.render("[Click anywhere to continue]", True, WHITE)
        text_rect3 = text.get_rect(center=((WIDTH/2), (WIDTH/2)+200))
        WIN.blit(text, text_rect3)
        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)
    font = pygame.font.Font(None, 36)
    font1 = pygame.font.Font(None, 48)
    start = None
    end = None

    run = True
    started = False
    display_instructions = True

    instruction(run, display_instructions, font, font1)

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
            if pygame.mouse.get_pressed()[0]: # left mouse click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                square = grid[row][col]
                if not start and square != end:
                    start = square
                    start.make_start()
                elif not end and square != start:
                    end = square
                    end.make_end()

                elif square != end and square != start:
                    square.make_barrier()
            elif pygame.mouse.get_pressed()[2]: # right mouse click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                square = grid[row][col]
                square.reset()
                if square == start:
                    start = None
                elif square == end:
                    end = None

            if event.type == pygame.KEYDOWN: # pressed key
                if event.key == pygame.K_SPACE and start and end: # pressed spacebar
                    for row in grid:
                        for square in row:
                            square.update_neighbors(grid)
                    
                    algo(lambda: draw(win, grid, ROWS, width), grid, start, end)
                if event.key == pygame.K_c: # pressed 'c' key 
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                if event.key == pygame.K_m:
                    display_instructions = True
                    instruction(run, display_instructions, font, font1)
                if event.key == pygame.K_ESCAPE: # pressed 'escape' key 
                    pygame.quit()
                    sys.exit()
    pygame.quit()

main(WIN, WIDTH)
