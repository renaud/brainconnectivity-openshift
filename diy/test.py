from tornado import ioloop, web, autoreload


class MainHandler(web.RequestHandler):
    def get(self):
        self.write("Hello, world11" + dbhost)

application = web.Application([
    (r"/", MainHandler),
])


dbhost = 'a'
dbport = '1'

def main(address, _dbhost, _dbport):
    global dbhost
    dbhost = _dbhost
    global dbport
    dbport = _dbport

    application.listen(8080, address)
    ioloop.IOLoop.instance().start()

# local debug
if __name__ == "__main__":
    address = "127.0.0.1"
    main(address, 'localhost', '3306')
