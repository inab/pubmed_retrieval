'''
Created on May 23, 2018

@author: jcorvi
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
def InitDataBase(parameters):
    global Session
    engine = create_engine(parameters['database_url'], echo=False)
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    return None

def getSession():
    return Session()