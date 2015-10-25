import heapq, time
import random
import pygame

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = ( 0,   0,   255)
#--
ORANGE = (255, 165, 0)
 
width  = 6
height = 6
margin = 1
size = [708, 708]
screen = pygame.display.set_mode(size)
 
class Grid(object):
    def __init__(self, x, y, blocked):
        self.blocked = blocked
        self.visited = False
        self.path = False
        self.x = x
        self.y = y
        self.parent = None
        self.next = None
        self.g = 0
        self.h = 0
        self.f = 0
    def __lt__(self, other):
        return self.f < other.f
    
class Gridworld(object):
    def __init__(self):
        self.open = []
        heapq.heapify(self.open)
        self.close = set()
        self.grids = []
        self.grid_height = 101
        self.grid_width = 101
        self.filename = ''

    def init_grid(self):
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                blocked = False
                if random.randint(1,100) < 30:
                    blocked = True
                self.grids.append(Grid(x, y, blocked))
        self.start = self.get_grid(random.randint(1,100), random.randint(1,100))
        self.end = self.get_grid(random.randint(1,100), random.randint(1,100))
##        self.last_visited = self.start
        self.start.blocked = False
        self.end.blocked = False
        self.start.path = True
        self.end.path = True

    def get_grid(self, x, y):
        return self.grids[x * self.grid_height + y]

    def create_file(self):
        opfile = open(self.filename,"w")
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                current_grid = self.get_grid(x, y)
                if current_grid is self.start:
                    opfile.write('S')
                elif current_grid is self.end:
                    opfile.write('G')
                elif current_grid.blocked:
                    opfile.write('b')
                else:
                    opfile.write('~')
            opfile.write('\n')
        opfile.close()
        
    def display_grid(self):
        pygame.display.set_caption("A star implementation")
        screen.fill(BLACK)
        done = False
        while done == False:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    done = True
                for grid in self.grids:
                        color = BLACK
                        if grid.blocked == False:
                            color = WHITE
                        #--
                        if grid.visited == True and grid.blocked == False:
                            color = BLUE
                        #--
                        if grid.path == True:
                            color = GREEN
                        #--
                        if grid == self.start:
                            color = RED
                        if grid == self.end:
                            color = ORANGE
                        #--
                        pygame.draw.rect(screen, color,
                             [(margin+width)*grid.x+margin, (margin+height)*grid.y+margin,
                              width, height])        
            pygame.display.flip()
##            time.sleep(0.5)

def main():
    pygame.init()
    for n in range(50):
        a = Gridworld()
        a.init_grid()
        a.filename = 'Mazes\\'+str(n+1)+'.txt'
        a.create_file()
##        a.display_grid()
    pygame.quit()
    
if __name__ == '__main__':
    main()
