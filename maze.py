import pygame
import sys
from collections import deque

# ================= CONFIG =================
WIDTH, HEIGHT = 600, 650
ROWS, COLS = 15, 15
CELL_SIZE = 600 // COLS
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
RED = (200, 0, 0)
GRAY = (200, 200, 200)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
BLUE=(0,0,180)

START = (0, 0)
END = (ROWS - 1, COLS - 1)

# ================= MAZE =================
maze = [
    [0,1,0,0,0,1,0,0,0,1,0,0,0,1,0],
    [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],
    [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0],
    [1,1,0,1,1,1,0,1,1,1,0,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,0,1,1,1,0,1,1,1,0],
    [0,0,0,0,0,0,0,1,0,0,0,1,0,0,0],
    [0,1,1,1,1,1,0,1,0,1,0,1,0,1,0],
    [0,0,0,1,0,0,0,0,0,1,0,0,0,1,0],
    [1,1,0,1,0,1,1,1,0,1,1,1,0,1,0],
    [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,0,1,1,1,0,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,0,1,0,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0]
]

# ================= INIT =================
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 42)

# ================= BUTTON =================
class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self):
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        txt = font.render(self.text, True, BLACK)
        screen.blit(txt, (self.rect.centerx - txt.get_width()//2,
                          self.rect.centery - txt.get_height()//2))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

# ================= SOLVERS =================
def bfs_path():
    queue = deque([START])
    parent = {START: None}
    while queue:
        cur = queue.popleft()
        if cur == END:
            break
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = cur[0]+dr, cur[1]+dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and maze[nr][nc] == 0 and (nr,nc) not in parent:
                parent[(nr,nc)] = cur
                queue.append((nr,nc))
    path = []
    cur = END
    while cur:
        path.append(cur)
        cur = parent[cur]
    return path[::-1]

def dfs_path():
    stack = [START]
    parent = {START: None}
    while stack:
        cur = stack.pop()
        if cur == END:
            break
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = cur[0]+dr, cur[1]+dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and maze[nr][nc] == 0 and (nr,nc) not in parent:
                parent[(nr,nc)] = cur
                stack.append((nr,nc))
    path = []
    cur = END
    while cur:
        path.append(cur)
        cur = parent[cur]
    return path[::-1]

BFS_PATH = bfs_path()
DFS_PATH = dfs_path()

# ================= DRAW =================
def draw_maze(player, solution=None):
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[r][c] == 1:
                pygame.draw.rect(screen, BLACK, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

    if solution:
        for r, c in solution:
            pygame.draw.rect(screen, YELLOW, (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.draw.rect(screen, GREEN, (START[1]*CELL_SIZE, START[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (END[1]*CELL_SIZE, END[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, ORANGE, (player[1]*CELL_SIZE, player[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

# ================= STATES =================
MENU, GAME, WIN = 0, 1, 2
state = MENU
algorithm = None
player = list(START)
user_path = [START]
show_solution = False

# ================= BUTTONS =================
start_bfs = Button("Start (BFS)", 200, 220, 200, 40)
start_dfs = Button("Start (DFS)", 200, 280, 200, 40)
reveal_btn = Button("Reveal Solution", 200, 360, 200, 40)
back_btn = Button("Back to Menu", 200, 420, 200, 40)
quit_btn = Button("Quit", 200, 480, 200, 40)

# ================= MAIN LOOP =================
running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if state == MENU:
                if start_bfs.clicked(pos):
                    algorithm = "BFS"
                    player = list(START)
                    user_path = [START]
                    show_solution = False
                    state = GAME
                if start_dfs.clicked(pos):
                    algorithm = "DFS"
                    player = list(START)
                    user_path = [START]
                    show_solution = False
                    state = GAME
                if quit_btn.clicked(pos):
                    running = False

            elif state == WIN:
                if reveal_btn.clicked(pos):
                    show_solution = True
                if back_btn.clicked(pos):
                    state = MENU
                if quit_btn.clicked(pos):
                    running = False

        if event.type == pygame.KEYDOWN and state == GAME:
            r, c = player
            move = None
            if event.key == pygame.K_UP and r > 0 and maze[r-1][c] == 0:
                move = (r-1, c)
            if event.key == pygame.K_DOWN and r < ROWS-1 and maze[r+1][c] == 0:
                move = (r+1, c)
            if event.key == pygame.K_LEFT and c > 0 and maze[r][c-1] == 0:
                move = (r, c-1)
            if event.key == pygame.K_RIGHT and c < COLS-1 and maze[r][c+1] == 0:
                move = (r, c+1)
            if move:
                player = list(move)
                user_path.append(move)

    if state == GAME and tuple(player) == END:
        state = WIN

    # ================= DRAW STATES =================
    if state == MENU:
        title = big_font.render("Maze Game", True, BLACK)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))
        start_bfs.draw(); start_dfs.draw(); quit_btn.draw()

    elif state == GAME:
        draw_maze(player)

    elif state == WIN:
        sol = BFS_PATH if algorithm == "BFS" else DFS_PATH
        draw_maze(player, sol if show_solution else None)

        t1 = big_font.render("YOU SOLVED THE MAZE!", True, GREEN)
        t2 = font.render(f"Your path length: {len(user_path)-1}", True, BLUE)
       # t3 = font.render(f"BFS shortest path: {len(BFS_PATH)-1}", True, BLACK)
        #t4 = font.render(f"DFS path length: {len(DFS_PATH)-1}", True, BLACK)
        t3 = font.render(f"BFS shortest path: {len(BFS_PATH)-1}", True, (0, 120, 255))
        t4 = font.render(f"DFS path length: {len(DFS_PATH)-1}", True, (180, 0, 180))

        screen.blit(t1, (120, 20))
        screen.blit(t2, (180, 70))
        screen.blit(t3, (180, 100))
        screen.blit(t4, (180, 130))

        reveal_btn.draw(); back_btn.draw(); quit_btn.draw()

    pygame.display.update()

pygame.quit()
sys.exit()

"""
FINAL FIXED VERSION
- No white screen bug
- Stable state transitions
- Correct BFS / DFS comparison
- Clean menu navigation
"""