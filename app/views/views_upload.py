# -*- coding: utf-8 -*-
import os
import datetime
import uuid
import tornado.gen
import tornado.concurrent
from app.views.views_auth import AuthHandler


class UploadHandler(AuthHandler):
    def check_xsrf_cookie(self):
        return True

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        yield self.post_response()

    @tornado.concurrent.run_on_executor
    def post_response(self):
        files = self.request.files["img"]
        imgs = []
        upload_path = os.path.join(
            os.path.dirname(
                os.path.dirname(__file__)
            ), "static/uploads"
        )

        if not os.path.exists(upload_path):
            os.mkdir(upload_path)

        for v in files:
            if len(self.request.headers.get('Content-Length')) >= (2 * 1024 * 1024):
                self.write(
                    dict(
                        code=3,
                    )
                )
                return

            type = os.path.splitext(v['filename'])[1]
            if type != ".jpg" and type != ".gif" and type != ".jpeg" and type != ".png":
                self.write(
                    dict(
                        code=2,
                    )
                )
                return

            prefix1 = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            prefix2 = uuid.uuid4().hex
            newname = prefix1 + prefix2 + os.path.splitext(v['filename'])[-1]
            with open(os.path.join(upload_path, newname), "wb") as up:
                up.write(v["body"])
            imgs.append(newname)

        self.write(
            dict(
                code=1,
                image=imgs[-1]
            )
        )
