# -*- coding: utf-8 -*-
import json
import tornado.gen
import tornado.concurrent
from app.views.views_common import CommonHandler
from app.models.crud import Database
from app.tools.forms import ChatForm


class MsgHandler(CommonHandler):
    def check_xsrf_cookie(self):
        return True

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        yield self.post_response()

    @tornado.concurrent.run_on_executor
    def post_response(self):
        form = ChatForm(self.fdata)
        data = Database.get_msg(int(form.data['vid']))
        result = []
        for v in data:
            result.append(json.loads(v.content))
        self.write(
            dict(
                data=result
            )
        )
