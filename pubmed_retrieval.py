import os
import sys
from ftplib import FTP
from datetime import datetime
import argparse
import ConfigParser
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

parser=argparse.ArgumentParser()
parser.add_argument('-o', help='Output Directory')
parser.add_argument('-p', help='Path Parameters')

args=parser.parse_args()
ftp=FTP("ftp.ncbi.nlm.nih.gov")
ftp.login("","")
parameters={}
if __name__ == '__main__':
    import pubmed_retrieval
    parameters = pubmed_retrieval.ReadParameters(args)     
    pubmed_retrieval.Main(parameters)
    
def ReadParameters(args):
    parameters_error=False
    parameters_obligation=False
    if(args.p!=None):
        Config = ConfigParser.ConfigParser()
        Config.read(args.p)
        parameters['output_directory']=Config.get('MAIN', 'output')
    else:
        parameters_obligation=True
    if(args.o!=None):
        parameters['output_directory']=args.o
    elif (parameters_obligation):
        print ("No output directory provided")
        parameters_error=False
    if(parameters_error):
        print("Please send the correct parameters.  You can type for --help ")
        sys.exit(1)
    return parameters
 
def Main(parameters):
    retrieval_output=parameters['output_directory']
    if not os.path.exists(retrieval_output):
        os.makedirs(retrieval_output)
    folder_name = 'baseline'
    source="/pubmed/baseline/"
    download(source, retrieval_output, folder_name)    
    folder_name = "updatefiles_"+str(datetime.now().date())
    source="/pubmed/updatefiles/"
    download(source, retrieval_output,folder_name)
            
def download(source, dest, folder_name):
    logging.info("Downloading Pubmed from  : " + source + ",  destination : "  + dest)
    work_dir = os.path.join(dest, folder_name)
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)
    ids_list=[]
    if(os.path.isfile(dest+"/list_files_downloaded.txt")):
        with open(dest+"/list_files_downloaded.txt",'r') as ids:
            for line in ids:
                ids_list.append(line.replace("\n",""))
        ids.close()
    
    ftp.cwd(source)
    filelist=ftp.nlst()
    with open(dest+"/list_files_downloaded.txt",'a') as list_files_downloaded:
        for file in filelist:
            if (file.endswith("xml.gz") & (file not in ids_list)):
                ftp.retrbinary("RETR "+file, open(os.path.join(work_dir,file),"wb").write)
                logging.info("Downloaded   : " + file)
                #download the md5 
                file_md5=file+".md5"
                ftp.retrbinary("RETR "+file_md5, open(os.path.join(work_dir,file_md5),"wb").write)   
                list_files_downloaded.write(file+"\n")
                list_files_downloaded.flush()
        list_files_downloaded.close()
    logging.info("Downloading Pubmed End")    