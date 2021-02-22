from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
Session = sessionmaker()

class Database():

    def __init__(self):
        #self.engine = create_engine('sqlite:///:memory:', echo=False)
        self.engine = create_engine('sqlite:///banco_imob_v2.sqlite3', echo=False)
        Base.metadata.create_all(self.engine)
        Session.configure(bind=self.engine)
        self.session = Session()

    