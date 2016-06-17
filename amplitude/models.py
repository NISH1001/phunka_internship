#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker

import settings

DeclarativeBase = declarative_base()

def db_connect():
    return create_engine(URL(**settings.DATABASE), echo=True)

def create_amplitude_table(engine):
    DeclarativeBase.metadata.create_all(engine)

class Amplitude(DeclarativeBase):
    __tablename__ = "amplitude"
    
    #pk                      = Column(Integer, primary_key=True)
    uuid                    = Column(String, primary_key=True)
    app                     = Column(String)

    # device info
    device_carrier          = Column(String)
    device_model            = Column(String)
    device_family           = Column( String)
    device_manufacturer     = Column(String)
    device_brand            = Column(String)
    platform                = Column(String)
    os_name                 = Column(String)
    device_id               = Column(String)

    # region info
    city                    = Column(String)
    country                 = Column(String)
    region                  = Column(String)
    language                = Column(String)
    location_lng            = Column(String)
    location_lat            = Column(String)

    event_time              = Column(String)
    client_event_time       = Column(String)
    profess_time            = Column(String)
    user_creation_time      = Column(String)
    client_upload_time      = Column(String)

    insert_id               = Column(String)
    event_type              = Column(String)
    event_id                = Column(String)
    library                 = Column(String)
    amplitude_event_type    = Column(String)
    version_name            = Column(String)
    ip_address              = Column(String)
    paying                  = Column(String)
    user_id                 = Column(String)

    def __str__(self):
        return str(self.uuid)


def main():
    engine = db_connect()
    Session = sessionmaker(bind=engine)
    session = Session()

if __name__ == "__main__":
    main()




