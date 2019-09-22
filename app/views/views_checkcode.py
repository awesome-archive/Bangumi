# -*- coding: utf-8 -*-
import tornado.gen
import tornado.concurrent
import io
from app.tools import verifycode
from app.views.views_common import CommonHandler


class CheckCodeHandler(CommonHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        imgio = io.BytesIO()
        img, code = verifycode.create_validate_code()
        img.save(imgio, 'GIF')
        self.write(imgio.getvalue())
        self.session["chkcode"] = code
