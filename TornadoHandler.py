import redis
import tornado.ioloop,tornado.web,tornado.websocket
from tornado.ioloop import PeriodicCallback

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('./index/index.html')

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.callback = PeriodicCallback(self.__send_message, 400)
        self.callback.start()

    def __send_message(self):
        redis_object = redis.Redis(host='localhost', port=6379,db=0)
        send_data = {"maze":redis_object.get('maze').decode('utf-8'),
                    "is_goal": redis_object.get('is_goal').decode('utf-8'),
                    "player_x": redis_object.get('player_x').decode('utf-8'),
                    "player_y": redis_object.get('player_y').decode('utf-8'),
                    "start_x": redis_object.get('start_x').decode('utf-8'),
                    "start_y": redis_object.get('start_y').decode('utf-8'),
                    "goal_x": redis_object.get('goal_x').decode('utf-8'),
                    "goal_y": redis_object.get('goal_y').decode('utf-8'),
                    }
        self.write_message(send_data)

    def on_close(self):
        self.callback.stop()

