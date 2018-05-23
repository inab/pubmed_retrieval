'''
Created on May 18, 2018

@author: jcorvi
'''
from sqlalchemy import exists
from DataBaseUtil import getSession

class DAO:
    def save(self, instance):
        session = getSession()
        try:
            session.add(instance)
            session.commit()
        except Exception as inst:
            print inst
            session.rollback()
            raise
        finally:
            session.close()
            
    def findByName(self, model_class, name):
        session = getSession()
        try:
            ret = session.query(exists().where(model_class.name==name)).scalar()
        except Exception as inst:
            print inst
            session.rollback()
            raise
        finally:
            session.close()  
            return ret  
        
    def findAllNames(self, model_class):
        session = getSession()
        try:
            ret = session.query(model_class.filename).all()
        except Exception as inst:
            print inst
            session.rollback()
            raise
        finally:
            session.close()  
            return ret   