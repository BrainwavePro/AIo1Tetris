import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
s_width = 800
s_height = 700
play_width = 300  # Play area width (10 blocks wide)
play_height = 600  # Play area height (20 blocks high)
block_size = 30  # Size of a single block

# Top-left position of the play area
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height - 50

# Shape formats
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# List of shapes and their corresponding colors
shapes = [S, Z, I, O, J, L, T]
shape_colors = [
    (0, 255, 0),    # S - Green
    (255, 0, 0),    # Z - Red
    (0, 255, 255),  # I - Cyan
    (255, 255, 0),  # O - Yellow
    (255, 165, 0),  # J - Orange
    (0, 0, 255),    # L - Blue
    (128, 0, 128)   # T - Purple
]

class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x  # X position on the grid
        self.y = y  # Y position on the grid
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # Rotation state

def create_grid(locked_positions={}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]  # 20x10 grid filled with black
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in locked_positions:
                grid[y][x] = locked_positions[(x, y)]
    return grid

def convert_shape_format(piece):
    positions = []
    shape_format = piece.shape[piece.rotation % len(piece.shape)]
    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j - 2, piece.y + i - 4))
    return positions

def valid_space(piece, grid):
    accepted_positions = [[(x, y) for x in range(10) if grid[y][x] == (0,0,0)] for y in range(20)]
    accepted_positions = [pos for sublist in accepted_positions for pos in sublist]
    formatted = convert_shape_format(piece)
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:  # Ignore positions above the grid
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (
        top_left_x + play_width/2 - label.get_width()/2,
        top_left_y + play_height/2 - label.get_height()/2
    ))

def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y
    for y in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + y * block_size), (sx + play_width, sy + y * block_size))
        for x in range(len(grid[y])):
            pygame.draw.line(surface, (128, 128, 128), (sx + x * block_size, sy), (sx + x * block_size, sy + play_height))

def clear_rows(grid, locked_positions):
    increment = 0
    for y in range(len(grid)-1, -1, -1):
        row = grid[y]
        if (0,0,0) not in row:
            increment += 1
            ind = y
            for x in range(len(row)):
                try:
                    del locked_positions[(x,y)]
                except:
                    continue
    if increment > 0:
        # Shift rows down
        for key in sorted(list(locked_positions), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + increment)
                locked_positions[newKey] = locked_positions.pop(key)
    return increment

def draw_next_shape(piece, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255,255,255))
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    shape_format = piece.shape[piece.rotation % len(piece.shape)]
    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, piece.color, (
                    sx + j*block_size,
                    sy + i*block_size,
                    block_size, block_size), 0)
    surface.blit(label, (sx + 10, sy - 30))

def draw_window(surface, grid, score=0):
    surface.fill((0,0,0))
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255,255,255))
    surface.blit(label, (top_left_x + play_width/2 - label.get_width()/2, 30))
    # Current Score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (255,255,255))
    sx = top_left_x - 200
    sy = top_left_y + 200
    surface.blit(label, (sx + 20, sy + 160))
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x], (
                top_left_x + x*block_size,
                top_left_y + y*block_size,
                block_size, block_size), 0)
    draw_grid(surface, grid)
    pygame.draw.rect(surface, (255, 0, 0), (
        top_left_x, top_left_y, play_width, play_height), 5)

def main():
    global grid
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0
    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()
        # Increase speed over time
        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.15:
                fall_speed -= 0.005
        # Piece falling
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y +=1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -=1
                change_piece = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -=1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x +=1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x +=1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -=1
                elif event.key == pygame.K_DOWN:
                    current_piece.y +=1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -=1
                elif event.key == pygame.K_UP:
                    current_piece.rotation +=1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -=1
        shape_pos = convert_shape_format(current_piece)
        # Add piece to grid
        for x, y in shape_pos:
            if y > -1:
                grid[y][x] = current_piece.color
        # Handle piece change
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10
        draw_window(win, grid, score)
        draw_next_shape(next_piece, win)
        pygame.display.update()
        if check_lost(locked_positions):
            run = False
    draw_text_middle(win, "YOU LOST", 80, (255,255,255))
    pygame.display.update()
    pygame.time.delay(2000)

def main_menu():
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle(win, 'Press any key to begin', 60, (255,255,255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()

# Set up the display
win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')

# Start the game
main_menu()
