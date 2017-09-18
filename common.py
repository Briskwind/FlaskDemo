""" 通用代码"""
import json

from flask import Response, jsonify
from flask import render_template
from flask import request
from flask.views import View


class JsonResponse(Response):
    """ json 化返回"""

    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(JsonResponse, cls).force_type(rv, environ)


class BaseView(View):
    """ BaseView"""

    def get_template_name(self):
        raise NotImplementedError()

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def dispatch_request(self):
        if request.method != 'GET':
            return 'Un Support Method !'

        context = {'users': self.get_users()}
        return self.render_template(context)
