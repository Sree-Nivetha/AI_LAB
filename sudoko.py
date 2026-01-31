import pygame
import sys
import time

# ================= CONFIG =================
WIDTH, HEIGHT = 540, 620
CELL = 60
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,180)
GRAY = (200,200,200)
GREEN = (0,180,0)
RED = (200,0,0)
LIGHTBLUE = (210,230,255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Game - Backtracking AI")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

# ================= BOARD =================
board = [
    [5,3,0,0,7,0,0,0,0],
    [6,0,0,1,9,5,0,0,0],
    [0,9,8,0,0,0,0,6,0],
    [8,0,0,0,6,0,0,0,3],
    [4,0,0,8,0,3,0,0,1],
    [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0],
    [0,0,0,4,1,9,0,0,5],
    [0,0,0,0,8,0,0,7,9]
]

original = [row[:] for row in board]
selected = None
solving = False

# ================= DRAW =================
def draw():
    screen.fill(WHITE)
    draw_selection()
    draw_numbers()
    draw_grid()
    draw_buttons()
    pygame.display.update()

def draw_grid():
    for i in range(10):
        thickness = 3 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (0, i*CELL), (540, i*CELL), thickness)
        pygame.draw.line(screen, BLACK, (i*CELL, 0), (i*CELL, 540), thickness)

def draw_numbers():
    for r in range(9):
        for c in range(9):
            if board[r][c] != 0:
                color = BLACK if original[r][c] != 0 else BLUE
                txt = font.render(str(board[r][c]), True, color)
                screen.blit(txt, (c*CELL+20, r*CELL+15))

def draw_selection():
    if selected:
        r,c = selected
        pygame.draw.rect(screen, LIGHTBLUE, (c*CELL, r*CELL, CELL, CELL))

def draw_buttons():
    pygame.draw.rect(screen, GRAY, (40,560,140,40))
    pygame.draw.rect(screen, GRAY, (200,560,140,40))
    pygame.draw.rect(screen, GRAY, (360,560,140,40))

    screen.blit(small_font.render("Solve",True,BLACK),(80,570))
    screen.blit(small_font.render("Reset",True,BLACK),(235,570))
    screen.blit(small_font.render("Quit",True,BLACK),(410,570))

# ================= LOGIC =================
def valid(num, pos):
    r,c = pos
    if num in board[r]: return False
    if num in [board[i][c] for i in range(9)]: return False

    br, bc = r//3, c//3
    for i in range(br*3, br*3+3):
        for j in range(bc*3, bc*3+3):
            if board[i][j] == num:
                return False
    return True

def find_empty():
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return r,c
    return None

# ================= OPTIMIZED BACKTRACKING =================
def solve():
    find = find_empty()
    if not find:
        return True
    r,c = find

    for num in range(1,10):
        if valid(num,(r,c)):
            board[r][c] = num
            draw()
            time.sleep(0.02)

            if solve():
                return True

            board[r][c] = 0
            draw()
            time.sleep(0.02)
    return False

# ================= MAIN LOOP =================
running = True
while running:
    clock.tick(FPS)
    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()

            if y < 540:
                selected = (y//CELL, x//CELL)

            # Solve
            if 40 < x < 180 and 560 < y < 600:
                solve()

            # Reset
            if 200 < x < 340 and 560 < y < 600:
                board = [row[:] for row in original]

            # Quit
            if 360 < x < 500 and 560 < y < 600:
                running = False

        if event.type == pygame.KEYDOWN and selected:
            r,c = selected
            if original[r][c] == 0:
                if pygame.K_1 <= event.key <= pygame.K_9:
                    num = event.key - pygame.K_0
                    if valid(num,(r,c)):
                        board[r][c] = num
                elif event.key == pygame.K_BACKSPACE:
                    board[r][c] = 0

pygame.quit()
sys.exit()
