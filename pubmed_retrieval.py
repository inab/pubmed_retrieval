import sys
import os

from ftplib import FTP
from datetime import datetime
import argparse
from model import PubMedRetrieval
from dao import DAO

parser=argparse.ArgumentParser()
parser.add_argument('-o', help='Output Directory')


args=parser.parse_args()
ftp=FTP("ftp.ncbi.nlm.nih.gov")
ftp.login("","")

if __name__ == '__main__':
    import pubmed_retrieval
    try:
        dest=args.o
    except Exception as inst:
        print( "Error: reading the parameters.")
        sys.exit(1) 
    if dest==None:
        print( "Error: complete the destination path.") 
        sys.exit(1)    
    if not os.path.exists(dest):
        print( "Error: the destination path does not exist.") 
        sys.exit(1) 
    pubmed_retrieval.Main(args)


def Main(args):
    dest=args.o
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
            ftp.retrbinary("RETR "+file, open(os.path.join(work_dir,file),"wb").write)
            pubmedRet = PubMedRetrieval(file,'1',datetime.now(),folder_name,'0','null','null')
            print file + " downloaded"
            #download the md5 
            file=file+".md5"
            ftp.retrbinary("RETR "+file, open(os.path.join(work_dir,file),"wb").write)   
            print file + " downloaded"
            dao.save(pubmedRet)