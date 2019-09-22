# -*- coding: utf-8 -*-
import tornado.gen
import tornado.concurrent
from app.tools.forms import RegistForm
from app.views.views_common import CommonHandler
from app.models.crud import Database


class RegistHandler(CommonHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        data = dict()
        data["site_title"] = "注册_" + self.site_name
        self.html("normal/regist.html", data=data)

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        yield self.post_response()

    @tornado.concurrent.run_on_executor
    def post_response(self):
        form = RegistForm(self.fdata)
        res = dict(code=0)
        if form.validate():
            if Database.create_regist_user(form):
                res["code"] = 1
        else:
            res = form.errors
            res["code"] = 0
        self.write(res)
