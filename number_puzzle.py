import pygame
import sys
import random
from collections import deque

# ================= CONFIG =================
WIDTH, HEIGHT = 420, 520
CELL = 120
FPS = 60
SHUFFLE_MOVES = 100   # increase for harder game

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,180)
GRAY = (200,200,200)
GREEN = (0,180,0)
RED = (200,0,0)

MENU, GAME, WIN = 0, 1, 2

# ================= PUZZLE =================
initial_state = (1,2,3,
                 4,0,6,
                 7,5,8)

goal_state = (1,2,3,
              4,5,6,
              7,8,0)

moves = {
    0:[1,3], 1:[0,2,4], 2:[1,5],
    3:[0,4,6], 4:[1,3,5,7], 5:[2,4,8],
    6:[3,7], 7:[4,6,8], 8:[5,7]
}

# ================= INIT =================
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8 Puzzle Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 36)

# ================= BUTTON =================
class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x,y,w,h)

    def draw(self):
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        txt = font.render(self.text, True, BLACK)
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

# ================= SOLVERS =================
def get_neighbors(state):
    res = []
    z = state.index(0)
    for m in moves[z]:
        s = list(state)
        s[z], s[m] = s[m], s[z]
        res.append(tuple(s))
    return res

def bfs():
    q = deque([(initial_state,[initial_state])])
    visited = {initial_state}
    while q:
        s,p = q.popleft()
        if s == goal_state:
            return p
        for n in get_neighbors(s):
            if n not in visited:
                visited.add(n)
                q.append((n,p+[n]))

def dfs(limit=20):
    stack = [(initial_state,[initial_state],0)]
    visited = set()
    while stack:
        s,p,d = stack.pop()
        if s == goal_state:
            return p
        if d < limit:
            visited.add(s)
            for n in get_neighbors(s):
                if n not in visited:
                    stack.append((n,p+[n],d+1))

BFS_PATH = bfs()
DFS_PATH = dfs()

# ================= SHUFFLE (SOLVABLE) =================
def shuffle_board(state, steps=SHUFFLE_MOVES):
    board = list(state)
    last = None
    for _ in range(steps):
        z = board.index(0)
        r,c = divmod(z,3)
        neighbors = []
        if r>0: neighbors.append(z-3)
        if r<2: neighbors.append(z+3)
        if c>0: neighbors.append(z-1)
        if c<2: neighbors.append(z+1)
        if last in neighbors and len(neighbors)>1:
            neighbors.remove(last)
        n = random.choice(neighbors)
        board[z], board[n] = board[n], board[z]
        last = z
    return board

# ================= DRAW =================
def draw_board(state):
    for i,val in enumerate(state):
        r,c = divmod(i,3)
        rect = pygame.Rect(c*CELL+30, r*CELL+30, CELL, CELL)
        pygame.draw.rect(screen, WHITE, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        if val != 0:
            t = big_font.render(str(val), True, BLUE)
            screen.blit(t, t.get_rect(center=rect.center))

# ================= BUTTONS =================
start_bfs = Button("Start BFS", 110, 180, 200, 40)
start_dfs = Button("Start DFS", 110, 240, 200, 40)
shuffle_btn = Button("Shuffle (Hard)", 90, 380, 240, 40)
back_btn = Button("Back to Menu", 110, 430, 200, 40)
quit_btn = Button("Quit", 110, 300, 200, 40)

# ================= GAME VARS =================
state = MENU
algorithm = None
board = list(initial_state)
user_moves = 0

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
                    board = shuffle_board(goal_state)
                    user_moves = 0
                    state = GAME
                if start_dfs.clicked(pos):
                    algorithm = "DFS"
                    board = shuffle_board(goal_state)
                    user_moves = 0
                    state = GAME
                if quit_btn.clicked(pos):
                    running = False

            elif state == GAME:
                if shuffle_btn.clicked(pos):
                    board = shuffle_board(goal_state)
                    user_moves = 0

            elif state == WIN:
                if back_btn.clicked(pos):
                    state = MENU

        if event.type == pygame.KEYDOWN and state == GAME:
            z = board.index(0)
            r,c = divmod(z,3)

            if event.key == pygame.K_UP and r < 2:
                ni = (r+1)*3 + c
            elif event.key == pygame.K_DOWN and r > 0:
                ni = (r-1)*3 + c
            elif event.key == pygame.K_LEFT and c < 2:
                ni = r*3 + (c+1)
            elif event.key == pygame.K_RIGHT and c > 0:
                ni = r*3 + (c-1)
            else:
                ni = None

            if ni is not None:
                board[z], board[ni] = board[ni], board[z]
                user_moves += 1

    if tuple(board) == goal_state and state == GAME:
        state = WIN

    # ================= DRAW STATES =================
    if state == MENU:
        title = big_font.render("8 Puzzle Game", True, BLACK)
        screen.blit(title, (130, 100))
        start_bfs.draw()
        start_dfs.draw()
        quit_btn.draw()

    elif state == GAME:
        draw_board(board)
        shuffle_btn.draw()

    elif state == WIN:
        draw_board(board)
        t1 = big_font.render("PUZZLE SOLVED!", True, GREEN)
        t2 = font.render(f"Your moves: {user_moves}", True, RED)
        t3 = font.render(f"BFS shortest: {len(BFS_PATH)-1}", True, RED)
        t4 = font.render(f"DFS moves: {len(DFS_PATH)-1}", True, RED)

        screen.blit(t1,(100,10))
        screen.blit(t2,(120,300))
        screen.blit(t3,(120,330))
        screen.blit(t4,(120,360))
        back_btn.draw()

    pygame.display.update()

pygame.quit()
sys.exit()
