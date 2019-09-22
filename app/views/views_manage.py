# -*- coding: utf-8 -*-
import tornado.gen
import tornado.concurrent
from app.views.views_common import CommonHandler
from app.models.crud import Database


class ManageHandler(CommonHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        data = dict()
        if self.name.decode(encoding='utf-8') == "admin":
            data["site_title"] = "后台管理_" + self.site_name
            data["video"] = self.page(Database.get_videos())
            self.html("admin/manage.html", data=data)
        else:
            data["site_name"] = self.site_name
            self.html("404.html", data=data)
