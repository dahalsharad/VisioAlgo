import pygame, sys, random, math
from collections import deque
from tkinter import messagebox, Tk

size = (width, height) = 800, 800
pygame.init()

win = pygame.display.set_mode(size)
pygame.display.set_caption("Dijkstra's Path Finding")
clock = pygame.time.Clock()

cols, rows = 50, 50
w = width // cols
h = height // rows

grid = []
queue, visited = deque(), []
path = []

class Spot:
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.f, self.g, self.h = 0, 0, 0
        self.neighbors = []
        self.prev = None
        self.wall = False
        self.visited = False

    def show(self, win, col, shape=1):
        if self.wall == True:
            col = (0, 0, 0)
        if shape == 1:
            pygame.draw.rect(win, col, (self.x * w, self.y * h, w - 1, h - 1))
        else:
            pygame.draw.circle(win, col, (self.x * w + w // 2, self.y * h + h // 2), w // 3)

    def add_neighbors(self, grid):
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y + 1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
def clickWall(pos, state):
    i = pos[0] // w
    j = pos[1] // h
    grid[i][j].wall = state

def place(pos):
    i = pos[0] // w
    j = pos[1] // h
    return i, j
    
for i in range(cols):
    arr = []
    for j in range(rows):
        arr.append(Spot(i, j))
    grid.append(arr)

for i in range(cols):
    for j in range(rows):
        grid[i][j].add_neighbors(grid)

def main():
    flag = False
    noflag = True
    startflag = False
    start = None
    end = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if pygame.mouse.get_pressed()[0]:
                    i, j = place(pygame.mouse.get_pos())
                    spot = grid[i][j]
                    if not start and spot != end:
                        start = spot
                        queue.append(start)
                        start.visited = True
                        start.wall = False
                    elif not end and spot != start:
                        end = spot
                        end.wall = False
                if pygame.mouse.get_pressed()[2]:
                    i, j = place(pygame.mouse.get_pos())
                    spot = grid[i][j]
                    if spot == start:
                        start = None
                    if spot == end:
                        end = None
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    clickWall(pygame.mouse.get_pos(), True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    startflag = True

        if startflag:
            if len(queue) > 0:
                current = queue.popleft()
                if current == end:
                    temp = current
                    while temp.prev:
                        path.append(temp.prev)
                        temp = temp.prev
                    if not flag:
                        flag = True
                        print("Done")
                    elif flag:
                        continue
                if flag == False:
                    for i in current.neighbors:
                        if not i.visited and not i.wall:
                            i.visited = True
                            i.prev = current
                            queue.append(i)
            else:
                if noflag and not flag:
                    Tk().wm_withdraw()
                    messagebox.showinfo("ERROR 404", "PATH NOT FOUND.")
                    noflag = False
                else:
                    continue

        win.fill((0, 20, 20))
        for i in range(cols):
            for j in range(rows):
                spot = grid[i][j]
                spot.show(win, (255, 255, 255))
                if spot in path:
                    spot.show(win, (192, 57, 43))
                elif spot.visited:
                    spot.show(win, (39, 174, 96))
                if spot in queue:
                    spot.show(win, (44, 62, 80))
                    spot.show(win, (39, 174, 96), 0)
                if spot == start:
                    spot.show(win, (255, 255, 0))
                if spot == end:
                    spot.show(win, (0, 120, 255))

        pygame.display.flip()
main()


