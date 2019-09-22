# -*- coding: utf-8 -*-
import tornado.gen
import tornado.concurrent
from app.models.crud import Database
from app.views.views_common import CommonHandler
from app.tools.forms import EditForm


class EditHandler(CommonHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        data = dict()
        if self.name.decode(encoding='utf-8') == "admin":
            id = self.get_argument("id", None)
            if id:
                data = dict()
                data["site_title"] = "编辑视频_" + self.site_name
                data["video"] = Database.get_video(id)
                self.html("admin/edit.html", data=data)
            else:
                self.write("编辑失败! <a href=\"/manage/\">点击返回</a>")
        else:
            data["site_name"] = self.site_name
            self.html("404.html", data=data)

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        yield self.post_response()

    @tornado.concurrent.run_on_executor
    def post_response(self):
        data = dict()
        if self.name.decode(encoding='utf-8') == "admin":
            form = EditForm(self.fdata)
            res = dict(code=0)
            if form.validate():
                if Database.update_video(form):
                    res["code"] = 1
            else:
                res = form.errors
                res["code"] = 0
            self.write(res)
        else:
            data["site_name"] = self.site_name
            self.html("404.html", data=data)
