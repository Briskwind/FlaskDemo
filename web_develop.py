import urllib.parse

from flask import Flask
from  werkzeug.routing import BaseConverter

#  实现 WSGI
import settings

app = Flask(__name__)

app.config.from_object(settings)


@app.route('/')
def hello_world():
    """ hello world"""

    return 'Hello world'


@app.route('/item/<item_id>/')
def item(item_id):
    return 'this item :{}'.format(item_id)


class ListConverter(BaseConverter):
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


@app.route('/list3/')
def list3():
    return 'Separator:{}, {}'.format('+', 111)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
