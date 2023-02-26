'''
Djisktra's shortest path algorithm using pygame
'''
from tkinter import messagebox, Tk
import pygame
import sys
#variable declerations
window_width = 800
window_height = 600
cols = 50
rows = 50
box_width = window_width // cols
box_height = window_height // rows
grid = []
queue = []
path = []
window = pygame.display.set_mode((window_width,window_height))

class Box:
    def __init__(self,i, j):
        self.x = i
        self.y = j
        self.startPos = False # define start marker box
        self.wall = False # define wall markers box
        self.target = False # define destination marker box
        self.queued = False
        self.visted = False
        self.neighbours = []
        self.prior = None

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * box_width, self.y * box_height, box_width - 2, box_height - 2)) # -2 pixel allows to draw boarders

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < cols - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])


#initializing grid
for i in range(cols):
    array = []
    for j in range(rows):
        array.append(Box(i,j))
    grid.append(array)

for i in range(cols):
    for j in range(rows):
        grid[i][j].set_neighbours()
start_box  = grid[0][0]
start_box.startPos = True
start_box.visted = True
queue.append(start_box)
def main():
    begin_search = False #algorthim trigger
    target_box_set = False # endpoint of search
    searching = True
    target_box = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                #Draw obstacle Wall
                if event.buttons[0]: #left mouse button pressed
                    i = x // box_width
                    j = y // box_height
                    grid[i][j].wall = True

                # Final destination
                if event.buttons[2] and not target_box_set: #right mouse button pressed
                    i = x // box_width
                    j = y // box_height
                    target_box = grid[i][j]
                    target_box.target = True
                    target_box_set = True
            if event.type == pygame.KEYDOWN and target_box_set:
                begin_search = True
        if begin_search:
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visted = True
                if current_box == target_box:
                    searching = False
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            neighbour.prior = current_box
                            queue.append(neighbour)
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("no solution", "no possible path")
                    searching = False

        window.fill((0, 0, 0))
        for i in range(cols):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (20,20,20))

                if box.queued:
                    box.draw(window, (200, 0, 0))
                if box.visted:
                    box.draw(window, (0, 200, 0))
                if box.startPos:
                    box.draw(window, (0, 200, 200))
                if box in path:
                    box.draw(window, (0, 0, 200))
                if box.wall:
                    box.draw(window, (90, 90, 90))
                if box.target:
                    box.draw(window, (200, 200, 0))
        pygame.display.flip()
main()
