import heapq, time
import random
import pygame

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = ( 0,   0,   255)
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
        self.no_path = False

    def init_grid(self):
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                blocked = False
                if random.randint(1,100) < 30:
                    blocked = True
                self.grids.append(Grid(x, y, blocked))
        self.start = self.get_grid(random.randint(1,100), random.randint(1,100))
        self.end = self.get_grid(random.randint(1,100), random.randint(1,100))

    def init_partial_maze(self, true_maze):
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                blocked = False
                self.grids.append(Grid(x, y, blocked))
        self.start = self.get_grid(true_maze.start.x, true_maze.start.y)
        self.make_copy(self.start, true_maze.start)
        self.end = self.get_grid(true_maze.end.x, true_maze.end.y)
        self.make_copy(self.end, true_maze.end)

    def read_maze(self, filename):
        x=0
        y=0
        text_file = open(filename, "r")
        txt = text_file.readlines()
        for line in txt:
            y=0
            for chars in line:
##                print('x: %d, y: %d' % (x, y))
                grid = self.get_grid(x,y)
                if str(chars) == '~':
                    grid.blocked = False
                elif str(chars) == 'b':
                    grid.blocked = True
                elif str(chars) == 'S':
                    self.start = grid
                    self.start.path = True
                elif str(chars) == 'G':
                    self.end = grid
                    self.end.path = True
                self.grids.append(grid)
                y = y+1
            x = x+1
        text_file.close()

    def make_copy(self, temp_grid, true_grid):
        temp_grid.blocked = true_grid.blocked
        temp_grid.visited = true_grid.visited
        temp_grid.path = true_grid.path
        temp_grid.x = true_grid.x
        temp_grid.y = true_grid.y
        temp_grid.parent = true_grid.parent
        temp_grid.next = true_grid.next
        temp_grid.g = true_grid.g
        temp_grid.h = true_grid.h
        temp_grid.f = true_grid.f
        
    def get_heuristic(self, grid):
        #return 10 * (abs(grid.x - self.end.x) + abs(grid.y - self.end.y))
        return (abs(grid.x - self.end.x) + abs(grid.y - self.end.y))

    def get_grid(self, x, y):
        return self.grids[x * self.grid_height + y]

    def get_partial_grid(self, partial_maze, x, y):
        return partial_maze.grids[x * self.grid_height + y]

    def expand_grid(self, grid):
        try:
            grids = []
            if grid.x < self.grid_width-1:
                grids.append(self.get_grid(grid.x+1, grid.y))
            if grid.y > 0:
                grids.append(self.get_grid(grid.x, grid.y-1))
            if grid.x > 0:
                grids.append(self.get_grid(grid.x-1, grid.y))
            if grid.y < self.grid_height-1:
                grids.append(self.get_grid(grid.x, grid.y+1))
            return grids
        except AttributeError:
            self.no_path = True

    def display_path(self):
        grid = self.end
        while grid.parent is not self.start:
            grid = grid.parent
            grid.path = True
##            print('path: grid: %d,%d' % (grid.x, grid.y))

    def check_probable_path(self, true_maze):
        done = True
        return_grid = self.end

        grid = self.end
        while grid.parent is not self.start and grid.parent is not None:
            grid = grid.parent
##            print('Path followed: %d,%d' % (grid.x, grid.y))
            true_grid = true_maze.get_grid(grid.x, grid.y)
            if true_grid.blocked:
                print('Blocked at: %d,%d' % (grid.x, grid.y))
                return_grid = grid.parent
                true_grid.path = True
            else:
                true_grid.path = True
##            print(grid.blocked)

        tgrid = self.end
        while tgrid is not return_grid and tgrid is not None:
            true_grid = true_maze.get_grid(tgrid.x, tgrid.y)
            true_grid.path = False
            true_grid.visited = True
            tgrid = tgrid.parent
        
        return return_grid
        
    def display_grid(self):
        pygame.display.set_caption("Repeated Forward A* Implementation")
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

    def update_partial_maze(self, true_maze, Curr_start):
        try:
            exp_grids = self.expand_grid(Curr_start)
            for exp_grid in exp_grids:
                self.make_copy(exp_grid, true_maze.get_grid(exp_grid.x, exp_grid.y))
        except :
            self.no_path = True

    def update_grid(self, exp, grid):
        #--exp.g = grid.g + 10
        exp.g = grid.g+1
        exp.h = self.get_heuristic(exp)
        exp.parent = grid
##        grid.next = exp
        exp.f = exp.h + exp.g

    def run_AStar(self):
        try:
            heapq.heappush(self.open, (self.start.f, self.start))
            while len(self.open):
                f, grid = heapq.heappop(self.open)
    ##            grid.visited = True
                self.close.add(grid)
                if grid is self.end:
                    self.display_path()
                    break
                exp_grids = self.expand_grid(grid)
                for exp_grid in exp_grids:
                    if not exp_grid.blocked and exp_grid not in self.close:
                        if (exp_grid.f, exp_grid) in self.open:
    ##                        if exp_grid.g > grid.g + 10:
                            if exp_grid.g > grid.g:
                                self.update_grid(exp_grid, grid)
                        else:
                            self.update_grid(exp_grid, grid)
                            heapq.heappush(self.open, (exp_grid.f, exp_grid))
        except:
            self.no_path = True
            return

    def path_finder(self,true_maze):
        start_time = time.clock()
        done = False
        while done == False:
            print('Starting at (x,y): %d,%d' % (self.start.x, self.start.y))
            self.update_partial_maze(true_maze, self.start)
            self.run_AStar()
            grid_reached = self.check_probable_path(true_maze)

            if grid_reached is self.end:
##                print('Done is True')
                done = True
            else:
##                print('Done is False')
                self.open = []
                self.close = set()
                self.start = grid_reached
##                self.update_partial_maze(true_maze, self.start)
                done = False
            if self.no_path:
                break
        end_time = time.clock()
        print('Running Time: ', (end_time - start_time))

def main():
    pygame.init()
    maze_number = input("Give Maze Number: ")
    filename = 'Mazes\\'+str(maze_number)+'.txt'
    a = Gridworld()
    a.init_grid()
    a.read_maze(filename)

    OGStart = a.start
    OGEnd = a.end

    a.start = OGEnd
    a.end = OGStart
    
    b = Gridworld()
    b.init_partial_maze(a)

    a.start = OGStart
    a.end = OGEnd
    a.display_grid()

    a.start = OGEnd
    a.end = OGStart
    
    b.path_finder(a)
    if b.no_path:
        print('A Path from Start to Goal cannot be found')

    a.start = OGStart
    a.end = OGEnd
    a.display_grid()
    
    b.display_grid()
    pygame.quit()
    
if __name__ == '__main__':
    main()
