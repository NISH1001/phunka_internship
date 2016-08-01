from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker

from hairist import settings

DeclarativeBase = declarative_base()

def db_connect():
    return create_engine(URL(**settings.DATABASE), echo=False)

def create_hairist_table(engine):
    DeclarativeBase.metadata.create_all(engine)

class Hairist(DeclarativeBase):
    __tablename__ = "hairist"

    id                      = Column(Integer, primary_key=True)
    yetkili                 =   Column(String) 
    kuafor_salonu_turu      =   Column(String) 
    calisma_saatleri        =   Column(String) 
    tatil_gunleri           =   Column(String) 
    koltuk_sayisi           =   Column(String) 
    kullanilan_markalar     =   Column(String) 
    telfon                  =   Column(String) 
    mobil                   =   Column(String) 
    adres                   =   Column(String) 
    ilce_il                 =   Column(String) 
    email                   =   Column(String) 
    latlng                  =   Column(String) 
    image_urls              =   Column(String) 
