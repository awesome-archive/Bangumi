# -*- coding: utf-8 -*-
import tornado.gen
import tornado.concurrent
from app.views.views_common import CommonHandler
from app.tools.forms import LoginForm


class LoginHandler(CommonHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        data = dict()
        data["site_title"] = "登录_" + self.site_name
        self.html("normal/login.html", data=data)

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        yield self.post_response()

    @tornado.concurrent.run_on_executor
    def post_response(self):
        form = LoginForm(self.fdata)
        res = dict(code=0)
        if form.validate():
            res["code"] = 1
            self.set_secure_cookie("name", form.data['name'])
        else:
            res = form.errors
            res["code"] = 0
        self.write(res)
