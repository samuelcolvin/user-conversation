import sys
import os
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.wsgi
import tornado.httpserver

from userchat.wsgi import application as django_app

cl = []

class SocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print('new connection')
        print(id(self))
        if self not in cl:
            cl.append(self)

    def on_close(self):
        print('Client disconnected')
        print(id(self))
        if self in cl:
            cl.remove(self)

    def on_message(self, message):
        print('got message: %r' % message)
        print(id(self))
        for c in cl:
            c.write_message(message)


def main(run_django, port):
    handlers = [('/ws/', SocketHandler)]
    if run_django:
        wsgi_app = tornado.wsgi.WSGIContainer(django_app)
        dj_handler = ('.*', tornado.web.FallbackHandler, {'fallback': wsgi_app})
        handlers.append(dj_handler)
    app = tornado.web.Application(handlers)
    http_server = tornado.httpserver.HTTPServer(app)
    port = int(os.environ.get('PORT', port))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    run_django, port = True, 8000
    if 'nodjango' in sys.argv:
        run_django = False
        # django is running separately so we run tornado on a different port
        port = 8001
    main(run_django, port)
