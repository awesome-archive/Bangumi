# -*- coding: utf-8 -*-
import tornado.web


class ManagePageUI(tornado.web.UIModule):
    def render(self, data):
        return self.render_string("ui/manage_page.html", data=data)


class TagsPageUI(tornado.web.UIModule):
    def render(self, data, name):
        return self.render_string("ui/tags_page.html", data=data, name=name)


class SearchPageUI(tornado.web.UIModule):
    def render(self, data, query):
        return self.render_string("ui/search_page.html", data=data, query=query)


class VClassPageUI(tornado.web.UIModule):
    def render(self, data, vclass):
        return self.render_string("ui/vclass_page.html", data=data, vclass=vclass)
