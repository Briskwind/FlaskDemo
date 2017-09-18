import urllib.parse

from flask import Flask
from flask import abort
from flask import redirect
from flask import request
from flask import url_for
from werkzeug.routing import BaseConverter

#  实现 WSGI
import settings
from common import JsonResponse, BaseView


# template_folder 是相对 app.py 文件的
app = Flask(__name__, template_folder='./templates')

app.config.from_object(settings)


@app.route('/')
def hello_world():
    """ hello world"""

    return 'Hello world'


@app.route('/item/<item_id>/')
def item(item_id):
    return 'this item :{}'.format(item_id)


class ListConverter(BaseConverter):
    """ 自定义 url 转换器"""

    def __init__(self, url_map, separator='+'):
        super(ListConverter, self).__init__(url_map)
        self.separator = urllib.parse.unquote(separator)

    def to_python(self, value):
        return value.split(self.separator)

    def to_url(self, values):
        return self.separator.join(BaseConverter.to_url(value)
                                   for value in values)


app.url_map.converters['list'] = ListConverter


@app.route('/list1/<list:page_names>/')
def list1(page_names):
    return 'Separator:{}, {}'.format('+', page_names)


@app.route('/list2/<list(separator="|"):page_names>/')
def list2(page_names):
    return 'Separator:{}, {}'.format('|', page_names)


@app.route('/create/1/')
def create():
    # 构造 url 并且重定向
    print('url1', url_for('create', id='2'))
    location = url_for('item', item_id='1', a=2)
    return redirect(location, code=301)


@app.route('/people/')
def people():
    """ no name redirect"""
    name = request.args.get('name', None)
    if not name:
        return redirect(url_for('login'))
    user_agent = request.headers.get('User-Agent')
    return 'Name:{}, User-Agent:{}'.format(name, user_agent)


@app.route('/login/', methods=['POST', 'GET'])
def login():
    """ 定义 get post 方法"""

    if request.method == 'POST':
        user_id = request.form.get('user_id', None)
        return 'User:{} login'.format(user_id)

    else:
        return 'Open login page'


@app.route('/secret/')
def secret():
    # 会显示未授权，可返回其他失败的状态码
    abort(401)
    print('never executed')


app.response_class = JsonResponse


@app.route('/hello/')
def hello_2():
    return {'message': 'Hello world!'}


@app.route('/customer_headers')
def headers():
    """ headers"""
    # {'headers': [1, 2, 3]} 是返回内容
    # 201 状态码
    # ('X-Response-Id', 100) 在 Renspone Headers 中
    return {'headers': [1, 2, 3]}, 201, [('X-Response-Id', 100)]


app.config.from_object(settings)


class UserView(BaseView):
    def get_template_name(self):
        print(1)
        return 'chapter3/session1/user.html'

    def get_users(self):
        return [{
            'username': 'fake',
            'avatar': 'avatar'
        }]


app.add_url_rule('/users', view_func=UserView.as_view('userview'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=app.debug)
