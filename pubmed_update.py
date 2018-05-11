import sys
import os
import pandas
from ftplib import FTP
from datetime import datetime
import argparse

parser=argparse.ArgumentParser()
parser.add_argument('-o', help='Output Directory')
parser.add_argument('-r', help='Remove All Before downloading, warning you have to be sure of remove al the PubMed Database')

args=parser.parse_args()
ftp=FTP("ftp.ncbi.nlm.nih.gov")
ftp.login("","")

if __name__ == '__main__':
    import pubmed_update
    try:
        dest=args.o
        remove=args.r
    except Exception as inst:
        print( "error reading destination path.")
        sys.exit(1) 
    if not os.path.exists(dest):
        print( "error the destination path does not exist.") 
        sys.exit(1) 
    pubmed_update.Main(args)
    

def Main(args):
    dest=args.o
    remove=args.r
    result_file = dest + "/update_history.csv"
    columns = ["name","operation","folder","date","time","message","result"]
    if(remove):
        for filename in os.listdir(dest):
            if (filename.endswith(".gz") | filename.endswith(".md5")):
                os.remove(os.path.join(dest, filename))
    if os.path.isfile(result_file):
        df = pandas.read_csv(result_file, header=0, index_col=0)
    else:
        df = pandas.DataFrame(columns=columns)
    df_=df.loc[df['name'] == 'baseline']
    if(len(df_)==0):
        download_baseline(df,result_file,dest)    
    download_updates(df,result_file,dest)
            
def download_updates(df,result_file,dest):
    source="/pubmed/updatefiles/"
    files_downloaded = df['name'].tolist()
    ftp.cwd(source)
    filelist=ftp.nlst()
    folder_name = "updatefiles_"+str(datetime.now().date())
    work_dir = os.path.join(dest, folder_name)
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)
    print "Pubmed Updates download Starting ..." 
    for file in filelist:
        if (file.endswith("xml.gz") & (file not in files_downloaded)):
            index = len(df.index) + 1
            df.at[index,'operation']="download"
            df.at[index,'message']="pending"
            df.at[index,'name']=file
            df.at[index,'folder']=folder_name
            ftp.retrbinary("RETR "+file, open(os.path.join(work_dir,file),"wb").write)
            print file + " downloaded"
            df.at[index,'date']=str(datetime.now().date())
            df.at[index,'time']=str(datetime.now().time())
            df.at[index,'message']="complete"
            df.at[index,'result']="success"
            df.to_csv(result_file)    
    print "Pubmed Update download Finished"     
    
def download_baseline(df,result_file,dest):
    source="/pubmed/baseline/"
    work_dir = os.path.join(dest, "baseline")
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)
    index = len(df.index) + 1    
    df.at[index,'name']='baseline'  
    df.at[index,'folder']='baseline'
    df.at[index,'operation']="download"
    df.at[index,'message']="pending"
    ftp.cwd(source)
    filelist=ftp.nlst()
    print "Pubmed BaseLine download Starting ..." 
    for file in filelist:
        if file.endswith("xml.gz"):
            ftp.retrbinary("RETR "+file, open(os.path.join(dest,file),"wb").write)
            print file + " downloaded"
    print "Pubmed BaseLine download Finished"  
    df.at[index,'date']=str(datetime.now().date())
    df.at[index,'time']=str(datetime.now().time())
    df.at[index,'message']="finished"
    df.at[index,'result']="success"
    df.to_csv(result_file)    