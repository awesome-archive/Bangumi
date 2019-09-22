# -*- coding: utf-8 -*-
import tornado.gen
import tornado.concurrent
from app.views.views_auth import AuthHandler
from app.tools.forms import UserProfileEditForm
from app.models.crud import Database
from app.params import data as xz


class ProfileHandler(AuthHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        data = dict()
        data["site_title"] = "个人资料_" + self.site_name
        data["user"] = Database.get_user(self.name)
        data["xz"] = xz['xing_zuo']
        self.html("normal/profile.html", data=data)

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        yield self.post_response()

    @tornado.concurrent.run_on_executor
    def post_response(self):
        form = UserProfileEditForm(self.fdata)
        res = dict(code=0)
        if form.validate():
            if Database.save_user(form):
                res["code"] = 1
        else:
            res = form.errors
            res["code"] = 0
        self.write(res)
