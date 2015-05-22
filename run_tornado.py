import sys
import os
import json
import time
import datetime
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.wsgi
import tornado.httpserver


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'userchat.settings')

import django
django.setup()

from userchat.wsgi import application as django_app
from chat.models import Message, Conversation

ACTIONS = {
    'join': 'join_conversation',
    'msg': 'new_message'
}

conversations = {}


class SocketHandler(tornado.websocket.WebSocketHandler):
    con = None
    customer = None
    operator = None

    def check_origin(self, origin):
        return True

    def open(self):
        print('new connection')
        # print(self.request)

    def convert_one_msg(self, message):
        if message.user:
            author = message.user.get_full_name()
        else:
            author = self.con.customer.name
        return {
            'text': message.text,
            'author': author,
            'timestamp': message.timestamp.strftime('%s')
        }

    def convert_msgs(self, messages):
        return json.dumps(list(map(self.convert_one_msg, messages)))

    def join_conversation(self, text):
        data = json.loads(text)
        con_id = int(data['conversation_id'])
        # TODO authentication
        # let this throw an error for now
        con = Conversation.objects.get(id=con_id)
        # TODO permission check
        if con_id in conversations:
            conversations[con_id].append(self)
        else:
            conversations[con_id] = [self]
        self.con = con
        self.customer = data['customer']
        self.operator = data['operator']
        self._ping_timer()
        messages = Message.objects.filter(conversation=con).select_related('user')
        messages = self.convert_msgs(messages)
        self.write_message('msgs:=' + messages)

    def new_message(self, text):
        m = Message.objects.create(conversation=self.con, text=text)
        messages = self.convert_msgs([m])
        print(messages)
        for hdl in conversations[self.con.id]:
            hdl.write_message('msgs:+' + messages)

    def on_message(self, data):
        action, data = data.split(':', 1)
        assert action in ACTIONS, '"%s" is not in valid actions: %s' % (action, ','.join(ACTIONS.keys()))
        func = getattr(self, ACTIONS[action])
        func(data)

    def _ping_timer(self):
        t = bytes(str(time.time()), 'ascii')
        self.ping(t)

    def on_pong(self, data):
        response_time = time.time() - float(data)
        print('ping time: %0.2fms' % (response_time * 1000))

    def on_close(self):
        print('Client disconnected')
        if self in conversations.get(self.con.id, {}):
            conversations[self.con.id].remove(self)


def schedule_func():
    for c in cl:
        c.write_message('testing')


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
    main_loop = tornado.ioloop.IOLoop.instance()
    # sched = tornado.ioloop.PeriodicCallback(schedule_func, 3000, io_loop=main_loop)
    # sched.start()
    main_loop.start()

if __name__ == '__main__':
    run_django, port = True, 8000
    if 'nodjango' in sys.argv:
        run_django = False
        # django is running separately so we run tornado on a different port
        port = 8001
    main(run_django, port)
