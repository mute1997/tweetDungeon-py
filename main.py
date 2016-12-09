import redis
import tweepy,time
import tornado.ioloop,tornado.web,tornado.websocket

from TornadoHandler import MainHandler
from TornadoHandler import WebSocketHandler
from StreamListener import StreamListener

def get_auth():
    consumer_token = ""
    consumer_secret = ""
    key = ""
    secret = ""

    auth = tweepy.OAuthHandler(consumer_token,consumer_secret)
    auth.set_access_token(key, secret)
    return auth

if __name__ == '__main__':
    #redis
    redis_object = redis.Redis(host='localhost', port=6379,db=0)
    redis_object.flushall()

    #tweepy
    api = tweepy.API(get_auth())
    stream = tweepy.Stream(auth=api.auth,listener=StreamListener())
    stream.filter(track=[u'#tweetDungeonLC'], async=True)

    #tornado
    application = tornado.web.Application([
        (r"/",MainHandler),
        (r"/ws",WebSocketHandler)
    ])
    application.listen(8080)
    tornado.ioloop.IOLoop.current().start()
