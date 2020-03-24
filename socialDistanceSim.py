import pygame
import sys
import random
import math
from pygame import gfxdraw

pygame.init()
#user vars
POPULATION = 100
dot_size = 15
SEED = None # used to seed our pseudo-random number generator (None = systime seed)
#end user vars

#CONSTS
WIDTH = 800
HEIGHT = 800
speed = 2.0
fps = 60 * speed
#end CONSTS
background_color = (42,42,44)

# set up
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Social Distancing Simulation -- Justin Stitt')
clock = pygame.time.Clock()
random.seed(SEED)
#end set up

dots = []#collection of 'Dot' objs


class Dot:
    """
    A 'Dot' functions as a node to simulate collision and change color based on its
    current infection status (type).
    """
    def __init__(self,x,y,type = 0,can_move = False):
        self.pos = [x,y]#(x,y) in 2d space
        self.size = dot_size#radius of dot to render
        self.color = (47, 245, 142)#default color (healthy, type = 0)
        self.type = type#default is healthy. (0 = healthy, 1 = infected)
        #movement
        self.can_move = can_move
        self.v = 2#velocity (hypotenuse)
        self.speed = [0,0]#(x,y) pixel travel speed per frame
        self.angle = math.pi/3#in radians

    def update(self):
        if(self.can_move):
            #self.speed[0] = self.v * math.cos(self.angle)
            #self.speed[1] = self.v * math.sin(self.angle)
            self.pos[0] += int(self.speed[0])#math.ceil rounds up our float to the nearest pixel
            self.pos[1] -= int(self.speed[1])#math.ceil rounds up our float to the nearest pixel
        self.check_collision()
        self.render()
    def render(self):
        #two steps to drawing an Antialiased shape. Outline, then filled
        pygame.gfxdraw.aacircle(screen,*self.pos,self.size,self.color)
        pygame.gfxdraw.filled_circle(screen,*self.pos,self.size,self.color)

    def check_collision(self):
        if(self.can_move == False):
            return
        if(self.pos[0] + self.size >= WIDTH or self.pos[0] - self.size <= 0):
            self.angle = math.pi - self.angle
            return
        elif(self.pos[1] + self.size >= HEIGHT or self.pos[1] - self.size <= 0):
            self.angle = 2 * math.pi - self.angle
            return
        for dot in dots:
            dist = distance(*self.pos,*dot.pos)
            if ( dist <= (2 * dot_size) and dot != self):
                ##TO DO
                self.angle = 2 * math.pi - self.angle#HOW DO I FIND THE RESULTING ANGLE AFTER COLLISION :( (perfect elastic collision)
                dot.color = (255,0,0)
                dot.type = 1
                return

def randomly_populate():
    """
    Populates our screen space with healthy dots
    """
    rx = 0
    ry = 0
    for x in range(POPULATION):
        dots.append(gen_random())

def gen_random():
    rx = random.randint(0 + dot_size, WIDTH - dot_size)#bounds for random x
    ry = random.randint(0 + dot_size, HEIGHT - dot_size)#bounds for random y
    to_add = Dot(rx,ry)
    if(check_overlap(rx,ry) == False):
        return to_add
    else:
        return gen_random()#recursively generate another random dot if this dot overlaps with any other dots

def check_overlap(rx,ry):#returns True if we are NOT overlapping any other dot
    for dot in dots:
        if(  distance(rx,ry,*dot.pos) < dot_size * 2 ):#we are overlapping
            return True
    return False

def distance(x1,y1,x2,y2):
    dist = math.sqrt( (x2-x1)**2 + (y2-y1)**2   )
    return dist

def exit():
    pygame.quit()
    sys.exit()


def update():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    #object update calls
    for dot in dots:
        dot.update()

def render():
    pass

randomly_populate()
dots[5].can_move = True
dots[5].speed = [1,2]

while True:
    screen.fill(background_color)
    update()
    render()
    pygame.display.flip()
    clock.tick(fps)
