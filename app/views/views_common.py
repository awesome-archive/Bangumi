# -*- coding: utf-8 -*-
import math
import tornado.web
from tornado.escape import utf8
from tornado.util import unicode_type
from werkzeug.datastructures import MultiDict
from app.models.crud import Database
from concurrent.futures import ThreadPoolExecutor
from app.params import data
from app.tools.session import Session


def write_error(self, stat, **kw):
    self.render("404.html", data=data)


tornado.web.RequestHandler.write_error = write_error


class CommonHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(1000)
    site_name = data["site_name"]

    def initialize(self):
        self.session = Session(self)

    def prepare(self):
        blacks = Database.get_black()
        for black in blacks:
            if self.request.remote_ip == black.ipaddr:
                self.redirect('/inblack/')
                break

    @property
    def params(self):
        data = self.request.arguments
        data = {
            k: list(
                map(
                    lambda val: str(val, encoding="utf-8"),
                    v
                )
            )
            for k, v in data.items()
        }
        return data

    @property
    def fdata(self):
        return MultiDict(self.params)

    @property
    def name(self):
        return self.get_secure_cookie("name", None)

    @property
    def user(self):
        if self.name:
            return Database.get_user(self.name)
        else:
            return None

    def page(self, model):
        page = self.get_argument("page", 1)
        page = int(page)
        total = model.count()
        if total:
            shownum = 24
            pagenum = int(math.ceil(total / shownum))
            if page < 1:
                page = 1
            if page > pagenum:
                page = pagenum
            offset = (page - 1) * shownum
            data = model.limit(shownum).offset(offset)
            prev_page = page - 1
            next_page = page + 1
            if prev_page < 1:
                prev_page = 1
            if next_page > pagenum:
                next_page = pagenum
            arr = dict(
                pagenum=pagenum,
                page=page,
                prev_page=prev_page,
                next_page=next_page,
                data=data
            )
        else:
            arr = dict(
                data=[]
            )
        return arr

    def html(self, template_name, **kwargs):
        if self._finished:
            raise RuntimeError("Cannot render() after finish()")
        html = self.render_string(template_name, **kwargs)

        js_embed = []
        js_files = []
        css_embed = []
        css_files = []
        html_heads = []
        html_bodies = []
        for module in getattr(self, "_active_modules", {}).values():
            embed_part = module.embedded_javascript()
            if embed_part:
                js_embed.append(utf8(embed_part))
            file_part = module.javascript_files()
            if file_part:
                if isinstance(file_part, (unicode_type, bytes)):
                    js_files.append(file_part)
                else:
                    js_files.extend(file_part)
            embed_part = module.embedded_css()
            if embed_part:
                css_embed.append(utf8(embed_part))
            file_part = module.css_files()
            if file_part:
                if isinstance(file_part, (unicode_type, bytes)):
                    css_files.append(file_part)
                else:
                    css_files.extend(file_part)
            head_part = module.html_head()
            if head_part:
                html_heads.append(utf8(head_part))
            body_part = module.html_body()
            if body_part:
                html_bodies.append(utf8(body_part))

        if js_files:
            js = self.render_linked_js(js_files)
            sloc = html.rindex(b'</body>')
            html = html[:sloc] + utf8(js) + b'\n' + html[sloc:]
        if js_embed:
            js = self.render_embed_js(js_embed)
            sloc = html.rindex(b'</body>')
            html = html[:sloc] + js + b'\n' + html[sloc:]
        if css_files:
            css = self.render_linked_css(css_files)
            hloc = html.index(b'</head>')
            html = html[:hloc] + utf8(css) + b'\n' + html[hloc:]
        if css_embed:
            css = self.render_embed_css(css_embed)
            hloc = html.index(b'</head>')
            html = html[:hloc] + css + b'\n' + html[hloc:]
        if html_heads:
            hloc = html.index(b'</head>')
            html = html[:hloc] + b''.join(html_heads) + b'\n' + html[hloc:]
        if html_bodies:
            hloc = html.index(b'</body>')
            html = html[:hloc] + b''.join(html_bodies) + b'\n' + html[hloc:]
        return self.write(html)
