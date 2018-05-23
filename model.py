'''
Created on May 18, 2018

@author: jcorvi
'''

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence

Base = declarative_base()

class PubMedRetrieval(Base):
    __tablename__ = 'pubmed_retrieval'
    id = Column(Integer, Sequence('id'), primary_key=True)
    filename = Column(String(250))
    download = Column(Integer)
    download_datetime = Column(String(250))
    download_path = Column(String(400))
    unzip = Column(Integer)
    unzip_datetime = Column(String(250))
    unzip_path = Column(String(400))
    def __repr__(self):
        return "<PubMedRetrieval(filename='%s', download='%s', download_datetime='%s',download_path='%s', unzip='%s', unzip_datetime='%s', unzip_path='%s')>" % (
                                self.filename, self.download, self.download_datetime, self.download_path, self.unzip, self.unzip_datetime, self.unzip_path)
    
    """Consctructor"""
    def __init__(self, filename, download,download_datetime,download_path,unzip, unzip_datetime,unzip_path):
        self.filename = filename
        self.download = download
        self.download_datetime = download_datetime
        self.download_path = download_path
        self.unzip = unzip
        self.unzip_datetime = unzip_datetime
        self.unzip_path = unzip_path