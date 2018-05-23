'''
Created on May 18, 2018

@author: jcorvi
'''
from sqlalchemy import exists
from __init__ import Session

class DAO:
    def save(self, instance):
        session = Session()
        try:
            session.add(instance)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
            
    def findByName(self, model_class, name):
        session = Session()
        try:
            ret = session.query(exists().where(model_class.name==name)).scalar()
        except:
            session.rollback()
            raise
        finally:
            session.close()  
            return ret  
        
    def findAllNames(self, model_class):
        session = Session()
        try:
            ret = session.query(model_class.filename).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()  
            return ret   