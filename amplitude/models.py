#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, Column, Integer, String, DateTime

import settings

DeclarativeBase = declarative_base()

def db_connect():
    return create_engine(URL(**settings.DATABASE))

def create_amplitude_table(engine):
    DeclarativeBase.metadata.create_all(engine)

class Amplitude(DeclarativeBase):
    __tablename__ = "amplitude"
    
    id = Column(Integer, primary_key=True)
    uuid = Column('uuid', String)
    app = Column('app', String)

    # device info
    device_carrier = Column('device_carrier', String)
    device_model = Column('device_model', String)
    device_family = Column('device_family', String)
    device_manufacturer = Column('device_manufacturer', String)
    device_brand = Column('device_brand', String)
    platform = Column('platform', String)
    os_name = Column('os_name', String)
    device_id = Column('device_id', String)

    # region info
    city = Column('city', String)
    country = Column('country', String)
    region = Column('region', String)
    language = Column('language', String)
    longitude = Column('longitude', String)
    latitude = Column('latitude', String)

    event_time = Column('event_time', DateTime)
    client_event_time = Column('client_event_time', DateTime)
    profess_time = Column('profess_time', DateTime)
    user_creation_time = Column('user_creation_time', DateTime)
    client_upload_time = Column('client_upload_time', DateTime)

    insert_id = Column('insert_id', String)
    event_type = Column('event_type', String)
    event_id = Column('event_id', String)
    library = Column('library', String)
    amplitude_event_type = Column('amplitude_event_type', String)
    version_name = Column('version_name', String)
    ip_addres = Column('ip_addres', String)
    paying = Column('paying', String)


def main():
    print(db_connect())

if __name__ == "__main__":
    main()

