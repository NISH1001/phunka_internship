from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker

import settings

DeclarativeBase = declarative_base()

def db_connect():
    return create_engine(URL(**settings.DATABASE), echo=False)

def create_amplitude_table(engine):
    DeclarativeBase.metadata.create_all(engine)

class Ticket(DeclarativeBase):
    __tablename__ = "tickets"

    ticket          = Column(Integer, primary_key=True, autoincrement=True)
    user            = Column(String)
    timestamp       = Column(String) 
    issue           = Column(String)
    
    def __str__(self):
        return str(self.user)

class Update(DeclarativeBase):
    __tablename__ = "updates"

    ticket          = Column(Integer, primary_key=True)
    user            = Column(String)
    timestamp       = Column(String) 
    issue           = Column(String)

    def __str__(self):
        return str(self.user)

class Increment(DeclarativeBase):
    __tablename__ = "increments"
    pk          = Column(String, primary_key=True)
    ticketstate = Column(Integer)


def main():
    engine = db_connect()
    Session = sessionmaker(bind=engine)
    session = Session()

if __name__ == "__main__":
    main()




