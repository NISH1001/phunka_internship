from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker

import settings

DeclarativeBase = declarative_base()

DB_USER = settings.DATABASE['username']
DB_PASS = settings.DATABASE['password']
DB_HOST = settings.DATABASE['host']
DB_PORT = settings.DATABASE['port']
DATABASE = settings.DATABASE['database']

connect_string = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(DB_USER, DB_PASS, DB_HOST, DB_PORT, DATABASE)

def db_connect():
    #return create_engine(URL(**settings.DATABASE), echo=False)
    return create_engine(connect_string, echo=False)

def create_amplitude_table(engine):
    DeclarativeBase.metadata.create_all(engine)

class Ticket(DeclarativeBase):
    __tablename__ = "tickets"

    ticket          = Column(Integer, primary_key=True, autoincrement=True)
    user            = Column(String(100))
    timestamp       = Column(String(100)) 
    issue           = Column(String(100))
    
    def __str__(self):
        return str(self.user)

class Update(DeclarativeBase):
    __tablename__ = "updates"

    ticket          = Column(Integer, primary_key=True)
    user            = Column(String(100))
    timestamp       = Column(String(100)) 
    issue           = Column(String(100))

    def __str__(self):
        return str(self.user)

class Increment(DeclarativeBase):
    __tablename__ = "increments"
    pk          = Column(String(100), primary_key=True)
    ticketstate = Column(Integer)


def main():
    engine = db_connect()
    Session = sessionmaker(bind=engine)
    session = Session()

if __name__ == "__main__":
    main()




