from fundscout.models import Base
from fundscout.models import Session
from fundscout.tests.app import app as application
from wsgiref.simple_server import make_server
import sqlalchemy
import threading
import time


class SQLLayer(object):

    @classmethod
    def setUp(cls):
        engine = sqlalchemy.create_engine('sqlite:///:memory:')
        Base.metadata.bind = engine
        Base.metadata.create_all(engine)
        Session.configure(bind=engine)

    @classmethod
    def tearDown(cls):
        Base.metadata.drop_all()


#
# Kudos to http://www.jeanphi.fr/ from Ghost.py
#
class ServerThread(threading.Thread):
    """Starts a Tornado HTTPServer from given WSGI application.

    :param app: The WSGI application to run.
    :param port: The port to run on.
    """
    def __init__(self, app, port=5000):
        self.app = app
        self.port = port
        super(ServerThread, self).__init__()

    def run(self):
        self.http_server = make_server('', self.port, self.app)
        self.http_server.serve_forever()

    def join(self, timeout=None):
        if hasattr(self, 'http_server'):
            self.http_server.shutdown()
            del self.http_server


class IntegrationLayer(object):
    server_class = ServerThread
    port = 5000

    @classmethod
    def create_app(cls):
        """Returns your WSGI application for testing."""
        return application

    @classmethod
    def tearDown(cls):
        """Stops HTTPServer instance."""
        cls.server_thread.join()

    @classmethod
    def setUp(cls):
        """Starts HTTPServer instance from WSGI application."""
        cls.server_thread = cls.server_class(cls.create_app(), cls.port)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        while not hasattr(cls.server_thread, 'http_server'):
            time.sleep(0.01)
