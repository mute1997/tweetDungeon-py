import redis
import random

class Maze:
    def __init__(self):
        self.is_goal = 0

        self.screen_height = 15
        self.screen_width = 29

        self.maze = [[0 for i in range(self.screen_width)] for j in range(self.screen_height)]

        self.row = int(self.screen_height / 2)
        self.col = int(self.screen_width / 2)
        #wall 0
        #load 1
        #player 2
        self.maze[self.row][self.col] = 1

        direction = [0,1,2,3]
        random.shuffle(direction)
        self.__generate_maze(direction,self.row,self.col)
        self.__init_player()
        self.__init_goal()

        self.write_data()

    def __init_player(self):
        for i in range(0,self.screen_height):
            for j in range(0,self.screen_width):
                if self.maze[i][j] == 1:
                    self.start_x = i
                    self.start_y = j
                    self.player_x = i
                    self.player_y = j
                    return 0

    def __init_goal(self):
        for i in reversed(range(0,self.screen_height)):
            for j in reversed(range(0,self.screen_width)):
                if self.maze[i][j] == 1:
                    self.goal_x = i
                    self.goal_y = j
                    return 0

    def __generate_maze(self,direction,row,col):
        for i in range(0,3):
            if self.__can_create(direction[i],row,col):
                if direction[i] == 0:
                    self.maze[row][col - 1] = 1;
                    self.maze[row][col - 2] = 1;
                    col -= 2
                elif direction[i] == 1:
                    self.maze[row][col + 1] = 1;
                    self.maze[row][col + 2] = 1;
                    col += 2
                elif direction[i] == 2:
                    self.maze[row + 1][col] = 1;
                    self.maze[row + 2][col] = 1;
                    row += 2
                elif direction[i] == 3:
                    self.maze[row - 1][col] = 1;
                    self.maze[row - 2][col] = 1;
                    row -= 2

                direction = [0,1,2,3]
                random.shuffle(direction)

                self.__generate_maze(direction,row,col)

    def __can_create(self,direction,row,col):
        if direction == 0:
            if col - 2 <= 0:
                return False
            else:
                if self.maze[row][col - 2] == 0:
                    return True
                else:
                    return False
        elif direction == 1:
            if col + 2 >= self.screen_width - 1:
                return False
            else:
                if self.maze[row][col + 2] == 0:
                    return True
                else:
                    return False
        elif direction == 2:
            if row + 2 >= self.screen_height - 1:
                return False
            else:
                if self.maze[row + 2][col] == 0:
                    return True
                else:
                    return False
        elif direction == 3:
            if row - 2 <= 0:
                return False
            else:
                if self.maze[row - 2][col] == 0:
                    return True
                else:
                    return False
        else:
            return False

    def write_data(self):
        redis_object = redis.Redis(host='localhost', port=6379,db=0)
        redis_object.flushall()
        redis_object.set('maze',self.maze)
        redis_object.set('is_goal',self.is_goal)
        redis_object.set('player_x',self.player_x)
        redis_object.set('player_y',self.player_y)
        redis_object.set('start_x',self.start_x)
        redis_object.set('start_y',self.start_y)
        redis_object.set('goal_x',self.goal_x)
        redis_object.set('goal_y',self.goal_y)
        redis_object.set('width',self.screen_width)
        redis_object.set('height',self.screen_height)

    def move_player(self,direction):
        if direction == 0:
            if self.player_y - 1 > 0 and self.maze[self.player_x][self.player_y - 1] == 1:
                self.player_y -= 1
        elif direction == 1:
            if self.player_y + 1 > self.screen_width - 1 and self.maze[self.player_x][self.player_y + 1] == 1:
                self.player_y += 1
        elif direction == 2:
            if self.player_x + 1 < self.screen_height - 1 and self.maze[self.player_x + 1][self.player_y] == 1:
                self.player_x += 1
        elif direction == 3:
            if self.player_x - 1 > 0 and self.maze[self.player_x - 1][self.player_y] == 1:
                self.player_x -= 1

        if self.player_x == self.goal_x and self.player_y == self.goal_y:
            self.is_goal = 1
        else:
            self.is_goal = 0

        self.write_data()

    def display_maze(self):
        for i in range(self.screen_height):
            for j in range(self.screen_width):
                if self.maze[i][j] == 0:
                    print("x ",end="")
                else:
                    print("  ",end="")
            print("")
        print("")
