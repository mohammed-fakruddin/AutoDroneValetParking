"""Djikstra's Path Finding"""

import pygame, sys, random, math
from collections import deque
from tkinter import messagebox, Tk
from djitellopy import Tello
import threading
import cv2

#size = (width, height) = 640, 480
size = (width, height) = 320, 240
pygame.init()
myfont = pygame.font.SysFont('Comic Sans MS', 10)
win = pygame.display.set_mode(size)
pygame.display.set_caption("Dijkttra's Path Finding")
clock = pygame.time.Clock()

#cols, rows = 64, 48
cols, rows = 5, 5

w = width//cols
h = height//rows
print('width:',w, ' ,height:',h)
grid = []
queue, visited = deque(), []
path = []
path_reverse=[]

heading = []
movement = []

not_flew = True

class Spot:
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.f, self.g, self.h = 0, 0, 0
        self.neighbors = []
        self.prev = None
        self.wall = False
        self.visited = False
        # if random.randint(0, 100) < 20:
        #     self.wall = True
        
    def show(self, win, col, shape= 1):
        if self.wall == True:
            col = (0, 0, 0)
        if shape == 1:
            pygame.draw.rect(win, col, (self.x*w, self.y*h, w-1, h-1))
        else:
            pygame.draw.circle(win, col, (self.x*w+w//2, self.y*h+h//2), w//3)
    
    def add_neighbors(self, grid):
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x+1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x-1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y+1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y-1])


def clickWall(pos, state):
    i = pos[0] // w
    j = pos[1] // h
    grid[i][j].wall = state

def buildDefaultWall():
    grid[0][4].wall = True
    grid[1][4].wall = True
    grid[3][4].wall = True
    grid[4][4].wall = True

    grid[3][3].wall = True
    grid[4][3].wall = True

    grid[0][3].wall = True
    grid[1][3].wall = True


#def place(pos):
#    i = pos[0] // w
#    j = pos[1] // h
#    return w, h

for i in range(cols):
    arr = []
    for j in range(rows):
        arr.append(Spot(i, j))
    grid.append(arr)

for i in range(cols):
    for j in range(rows):
        grid[i][j].add_neighbors(grid)

    
#start = grid[cols//2][rows//2]
start = grid[2][4]
#end = grid[cols-50][rows - cols//2]
#end = grid[random.randint(0, 4)][random.randint(0, 2)]
end = grid[0][0]
start.wall = False
end.wall = False

queue.append(start)
start.visited = True
def generate_flight_path(path):
    
    path_copy = path.copy()
    path_copy.reverse()
    i=0
    prev_x = path_copy[0].x
    prev_y = path_copy[0].y
    for p in path_copy:
        print('generating path for:', p.x, p.y)
        #if (prev_x - p.x) == 0 and (prev_y-p.y) == 0:
        #    heading.append('north')
        #    movement.append('forward')
        if (prev_x - p.x) == 1 and (prev_y-p.y) == 0:
            heading.append('west')
            movement.append('forward')
           
        elif (prev_x - p.x) == -1 and (prev_y-p.y) == 0:
            heading.append('east')
            movement.append('forward')
            
        elif (prev_x - p.x) == 0 and (prev_y-p.y) == 1:
            heading.append('north')
            movement.append('forward')
           
        elif (prev_x - p.x) == 0 and (prev_y-p.y) == -1:
            heading.append('south')
            movement.append('forward')
           
    
        prev_x = p.x
        prev_y = p.y
    for i in range(len(heading)):
        print(heading[i])
    t = ','.join(heading)
    print("*************************")
    print(t)
    print("*************************")


def initializeTello():
    myDrone = Tello()
    myDrone.connect()
    myDrone.for_back_velocity = 0
    myDrone. left_right_velocity = 0
    myDrone.up_down_velocity = 0
    myDrone.yaw_velocity = 0
    myDrone.speed = 0
    print('BATTERY LEVELS:', myDrone.get_battery())
    myDrone.streamoff()
    myDrone.streamon()
    return myDrone

def fly_flight_path():
    myDrone = initializeTello()
    myDrone.takeoff()
    myDrone.move_up(50)
    prev_direction = "north"
    img_width_original = 320
    img_height_original = 240

    origin = (25, 25)
    thickness = 2
    fontScale = 1
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (0,0,255)

    for direction in heading:
        print('flying to:', direction)
        frame_read = myDrone.get_frame_read()
        image = frame_read.frame
        image = cv2.resize(image, (img_width_original, img_height_original))

        if direction == 'north': 
            #if prev direction is west - clockwise
            #if prev direction is east - counter clockwise
            if prev_direction == 'west':
                myDrone.rotate_clockwise(90)
            elif prev_direction == 'east': #east
                myDrone.rotate_counter_clockwise(90)
            myDrone.move_forward(25)
           
        elif direction == 'east':
            #if prev direction is north - clockwise
            #if prev direction is south - counter clockwise
            if (prev_direction == 'north'):
                myDrone.rotate_clockwise(90)
            elif(prev_direction == 'south'):
                myDrone.rotate_counter_clockwise(90)
            myDrone.move_forward(25)
                    
        elif (direction == 'west'):
            #if prev direction is north - counter clockwise
            #if prev direction is south - clockwise
            if (prev_direction == 'north'):
                myDrone.rotate_counter_clockwise(90)
            elif (prev_direction == 'south'):
                myDrone.rotate_clockwise(90)
            myDrone.move_forward(25)
        
        elif direction == 'south':
            #if prev direction is east - clockwise
            #if prev direction is south - counter clockwise
            if (prev_direction == 'west'):
                myDrone.rotate_counter_clockwise(90)
            elif (prev_direction == 'east'):
                myDrone.rotate_clockwise(90)
            myDrone.move_forward(25)
        # store the current direction to prev direction
        # display the image
        prev_direction = direction
        cv2.putText(image, direction, origin, font,
                    fontScale, color, thickness, cv2.LINE_AA)
        cv2.imshow("Path", image)
        key=cv2.waitKey(1) & 0xff
        if key==27:
            break
    myDrone.land()
    myDrone.end()
    cv2.destroyAllWindows()

def main():
    flag = False
    noflag = True
    startflag = False
    not_flew = True
    buildDefaultWall()
    x = threading.Thread(target=fly_flight_path, daemon=True)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if pygame.mouse.get_pressed():
                    clickWall(pygame.mouse.get_pos(), True)
                if pygame.mouse.get_pressed()[2]:
                    clickWall(pygame.mouse.get_pos(), False)
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    clickWall(pygame.mouse.get_pos(), True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
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
                        for p in path:
                            print(p.x, p.y)
                        generate_flight_path(path)
                        path_reverse = path.copy()
                        path_reverse.reverse()
                        if not_flew:
                            not_flew = False
                            #fly_flight_path()
                            x.start()
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
                    messagebox.showinfo("No Solution", "There was no solution" )
                    noflag = False
                else:
                    continue


        win.fill((0, 20, 20))
        for i in range(cols):
            for j in range(rows):
                spot = grid[i][j]
                spot.show(win, (44, 62, 80))
                if spot in path:
                    #spot.show(win, (192, 57, 43))
                    spot.show(win, (255, 255, 0))
                    t = ','.join(heading)
                    textsurface = myfont.render(t, False, (255, 255, 255))
                    win.blit(textsurface, ((end.x+1)*w*0.50, (end.y+1)*h*0.5))
                    
                elif spot.visited:
                    spot.show(win, (39, 174, 96))
                if spot in queue:
                    spot.show(win, (44, 62, 80))
                    spot.show(win, (39, 174, 96), 0)
                if spot == start:
                    spot.show(win, (0, 255, 200))
                    textsurface = myfont.render('Start', False, (0, 0, 0))
                    win.blit(textsurface, ((start.x)*w*1.1, (start.y)*h*1.1))
                    
                if spot == end:
                    spot.show(win, (0, 120, 255))
                    textsurface = myfont.render('End', False, (0, 0, 0))
                    win.blit(textsurface, ((end.x)*w*1.1, (end.y)*h*1.1))
                
        

        pygame.display.flip()


main()
