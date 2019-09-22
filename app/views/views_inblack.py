# -*- coding: utf-8 -*-
import tornado.gen
import tornado.concurrent


class InBlackHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        self.render("inblack.html")
