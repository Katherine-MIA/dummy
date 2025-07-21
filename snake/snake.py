import pygame
import math
import random
import tkinter as tk
from tkinter import messagebox

pygame.init()

class Cube(object):
    rows = 20
    w = 500
    def __init__(self, start, dirnx=1, dirny=0, color=(255,0,0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, drnx, drny):
        self.dirnx = drnx
        self.dirny = drny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1,dis-2,dis-2))
        #draw eyes on the head of the snake (approximate copied math, could stand to improve)
        if eyes:
            center = dis//2
            radius = 3
            circle_middle_l = (i*dis+center-radius, j*dis+8)
            circle_middle_r = (i * dis + dis - radius * 2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circle_middle_l, radius)
            pygame.draw.circle(surface, (0,0,0), circle_middle_r, radius)

class Snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        #create head of the snake that will be a cube at position (initial position the snake starts at (10,10))
        self.head = Cube(pos)
        #all cubes that constitute the snake are going to be ordered into the body list
        self.body.append(self.head)
        #direction for x and y, for keeping track of which direction snake moves in
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        #A list of all possible keys accounted for by pygame having
        #value 1 for the keys that have been pressed and 0 for the rest
        keys = pygame.key.get_pressed()
        for key in keys:
            if keys[pygame.K_LEFT]:
                self.dirnx = -1
                self.dirny = 0
                #key -> current position of the head of the snake
                #value -> turn direction
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            elif keys[pygame.K_RIGHT]:
                self.dirnx = 1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]

            elif keys[pygame.K_UP]:
                self.dirnx = 0
                self.dirny = -1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            elif keys[pygame.K_DOWN]:
                self.dirnx = 0
                self.dirny = 1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            #for each cube in the body get the position
            p = c.pos[:]
            #check if the position of c = cube exists in turns
            if p in self.turns:
                #at p position in turns there will be the way which the head should turn
                turn = self.turns[p]
                #move the cube at that position at the new position given by turn
                c.move(turn[0], turn[1])
                #when reaching the last cube the turn gets removed so that the cubes won't turn
                #again if the position is revisited (the cubes should move only when keys are pressed)
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                #if the cube is next to the left edge and hat to turn left then it gets transported
                #to the other side of the board on the same row (c.rows-1, c.pos[1])
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                #if cube next to right edge going right it gets transported to the left side on the same row
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0, c.pos[1])
                #if cube has to move upwards and there's no more grid it gets transported down
                #on the lower edge of the grid on the same column
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows-1)
                #when cube has to move down and runs out of grid, it gets transported to the first
                #square below the upper edge
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                #aside from the special cases the cubes keep advancing their position
                #in the direction specified by turn
                else: c.move(c.dirnx,c.dirny)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i==0:
                c.draw(surface, True)
            else:
                c.draw(surface)

def draw_grid(w, rows, surface):
    size_between = w // rows

    x = 0
    y = 0
    #for every row draw a line at x and y spaced by sizeBetween length
    for l in range(rows):
        x += size_between
        y = y + size_between
        #vertical line starting at (x,0) and ending at (x,w) -> length of the screen (since it's square width variable will suffice)
        pygame.draw.line(surface, (255,255,255), (x,0), (x,w))
        #horizontal line starting at the position (0,y) ending at (w,y)->width of the screen
        pygame.draw.line(surface, (255,255,255), (0,y), (w,y))

def redraw_window(surface):
    global rows, width, s, snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    #turn surface into grid
    draw_grid(width, rows, surface)
    #update display
    pygame.display.update()

def randomSnack(rows, snek):
    #global rows
    positions = snek.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else: break
    return (x, y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject,content)
    try:
        root.destroy()
    except: pass

def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    #create window that will become grid
    win = pygame.display.set_mode((width, width))
    s = Snake((255, 0, 0),(10, 10))
    snack = Cube(randomSnack(rows, s), color=(0,250,0))
    flag = True
    clock = pygame.time.Clock()
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        #turn window into grid
        s.move()
        if s.body[0].pos == snack.pos:
            s.add_cube()
            snack = Cube(randomSnack(rows, s), color=(0,250,0))
        #check all cubes in the body of the snake
        #if a position of a cube coincides with the position of another cube in the body
        #it will be treated as a collision and cause the game to be over and show the score
        #Then the game gets reset with a snake the length of 1 cube in the starting position (10,10)
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                title = 'Game Over! '
                message = 'Score: ' + str(len(s.body)) + '\n' + 'Play Again'
                message_box(title, message)
                s.reset((10, 10))
                break

        redraw_window(win)
        #pygame.event.pump()

main()
# for event in pygame.event.get():
#   if event.type == pygame.QUIT:
#      flag = False