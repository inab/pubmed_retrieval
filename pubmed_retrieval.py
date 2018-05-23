
import os

from ftplib import FTP
from datetime import datetime
import argparse
from model import PubMedRetrieval
from dao import DAO
import ConfigParser
from DataBaseUtil import InitDataBase

parser=argparse.ArgumentParser()
parser.add_argument('-o', help='Output Directory')
parser.add_argument('-u', help='SQLITE Database URL')
parser.add_argument('-p', help='Path Parameters')

args=parser.parse_args()
ftp=FTP("ftp.ncbi.nlm.nih.gov")
ftp.login("","")
parameters={}
if __name__ == '__main__':
    import pubmed_retrieval
    parameters = pubmed_retrieval.ReadParameters(args)     
    InitDataBase(parameters)
    pubmed_retrieval.Main(parameters)
    
def ReadParameters(args):
    if(args.p!=None):
        Config = ConfigParser.ConfigParser()
        Config.read(args.p)
        parameters['database_url']=Config.get('DATABASE', 'url')
        parameters['output_directory']=Config.get('MAIN', 'output')
    if(args.u!=None):
        parameters['database_url']=args.u
    if(args.o!=None):
        parameters['output_directory']=args.o
    return parameters
    
def Main(parameters):
    dest=parameters['output_directory']
    retrieval_output = dest + "/retrieval/"
    if not os.path.exists(retrieval_output):
        os.makedirs(retrieval_output)
    folder_name = 'baseline'
    source="/pubmed/baseline/"
    download(source, retrieval_output, folder_name)    
    folder_name = "updatefiles_"+str(datetime.now().date())
    source="/pubmed/updatefiles/"
    download(source, retrieval_output,folder_name)
            
def download(source,dest, folder_name):
    dao = DAO()
    work_dir = os.path.join(dest, folder_name)
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)
    files_downloaded = dao.findAllNames(PubMedRetrieval)
    files_list_downloaded = [row.filename for row in files_downloaded ]
    ftp.cwd(source)
    filelist=ftp.nlst()
    for file in filelist:
        if (file.endswith("xml.gz") & (file not in files_list_downloaded)):
            print file
            ftp.retrbinary("RETR "+file, open(os.path.join(work_dir,file),"wb").write)
            pubmedRet = PubMedRetrieval(file,'1',datetime.now(),folder_name,'0','null','null')
            print file + " downloaded"
            #download the md5 
            file=file+".md5"
            ftp.retrbinary("RETR "+file, open(os.path.join(work_dir,file),"wb").write)   
            print file + " downloaded"
            dao.save(pubmedRet)