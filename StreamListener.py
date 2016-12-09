import tweepy
from Maze import Maze

class StreamListener(tweepy.StreamListener):
    def __init__(self):
        super(StreamListener,self).__init__()
        self.maze = Maze()
        self.maze.display_maze()

    #データ受信時
    def on_status(self, status):
        print(status.text)
        if status.text.find('up') != -1:
            self.maze.move_player(0)
        elif status.text.find('down') != -1:
            self.maze.move_player(1)
        elif status.text.find('right') != -1:
            self.maze.move_player(2)
        elif status.text.find('left') != -1:
            self.maze.move_player(3)

    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            return False
