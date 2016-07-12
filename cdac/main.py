
import tornado.httpserver
import tornado.httpclient
import tornado.ioloop
import tornado.web
import tornado.options
from tornado import autoreload
import os
import pandas as pd

from tornado.options import options, define

define('port', default='8000', help='port where server is running')


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html', data=None	)


class StateLiteracy(tornado.web.RequestHandler):
	def get(self):
		data = pd.read_csv('state-literacy.csv')
		self.render('index.html', data=data.to_html())

class GenderLiteracy(tornado.web.RequestHandler):
	def get(self):
		data = pd.read_csv('gender-literacy.csv')
		self.render('index.html', data=data.to_html())


if __name__ == '__main__':
	tornado.options.parse_command_line()

	for d in os.listdir(os.getcwd()):
		autoreload.watch(os.path.abspath(os.path.abspath(d)))

	app = tornado.web.Application(handlers=[(r'/', MainHandler),
											(r'/state', StateLiteracy),
											(r'/gender', GenderLiteracy)],
								  autoreload=True,
								  templates_path=os.getcwd(),
								  static_path=os.getcwd())

	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()