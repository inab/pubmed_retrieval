#Data Base Connection
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import ConfigParser 

Config = ConfigParser.ConfigParser()
Config.read('config.properties')

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

url = ConfigSectionMap("DATABASE")['url']
engine = create_engine("sqlite:////home/jcorvi/sqlite_databases/bio_databases/bio_databases.db", echo=False)
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)

