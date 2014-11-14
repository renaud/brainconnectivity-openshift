from datetime import date
from tornado import ioloop, web, autoreload
import simplejson as json
import pymysql
from pymysql import escape_string
import math, os, codecs
import Counter
from collections import defaultdict
import ABA

class MainHandler(web.RequestHandler):
    def get(self):
        self.write("Hello, world5")

application = web.Application([
    (r"/", MainHandler),
])

def main(address):
    application.listen(8080, address)
    ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    address = "127.0.0.1"
    main(address)
