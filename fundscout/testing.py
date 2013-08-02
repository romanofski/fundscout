from fundscout.models import Base
from fundscout.models import Session
import sqlalchemy


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
