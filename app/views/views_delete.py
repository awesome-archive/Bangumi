# -*- coding: utf-8 -*-
import tornado.gen
import tornado.concurrent
from app.models.crud import Database
from app.views.views_common import CommonHandler


class DeleteHandler(CommonHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        data = dict()
        if self.name.decode(encoding='utf-8') == "admin":
            id = self.get_argument("id", None)
            if id:
                if Database.delete_video(id):
                    self.write("删除成功! <a href=\"/manage/\">点击返回</a>")
                else:
                    self.write("删除失败! <a href=\"/manage/\">点击返回</a>")
            else:
                self.write("删除失败! <a href=\"/manage/\">点击返回</a>")
        else:
            data["site_name"] = self.site_name
            self.html("404.html", data=data)
