# -*- coding: utf-8 -*-
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

from tornado.options import define, options
from app.configs import configs
from app.urls import urls

define("port", type=int, default=8000, help="运行端口")
tornado.options.parse_command_line()


class CustomApplication(tornado.web.Application):
    def __init__(self):
        settings = configs
        handlers = urls
        super(CustomApplication, self).__init__(handlers=handlers, **settings)


def create_http_server():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(CustomApplication())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
