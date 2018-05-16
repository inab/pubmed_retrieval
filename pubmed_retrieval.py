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
    import pubmed_retrieval
    try:
        dest=args.o
        remove=args.r
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
    remove=args.r
    result_file = dest + "/index.csv"
    columns = ["name","date","time","retrieval","folder"]
    if(remove):
        for filename in os.listdir(dest):
            if (filename.endswith(".gz") | filename.endswith(".md5")):
                os.remove(os.path.join(dest, filename))
    if os.path.isfile(result_file):
        df = pandas.read_csv(result_file, header=0, index_col=0)
    else:
        df = pandas.DataFrame(columns=columns)
    df_=df.loc[df['folder'] == 'baseline']
    retrieval_output = dest + "/retrieval/"
    if not os.path.exists(retrieval_output):
        os.makedirs(retrieval_output)
    
    if(len(df_)==0):
        folder_name = 'baseline'
        source="/pubmed/baseline/"
        download(source, df,result_file,retrieval_output, folder_name)    
    folder_name = "updatefiles_"+str(datetime.now().date())
    source="/pubmed/updatefiles/"
    download(source, df,result_file,retrieval_output, folder_name)
            
def download(source,df,result_file,dest, folder_name):
    work_dir = os.path.join(dest, folder_name)
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)
    files_downloaded = df['name'].tolist()
    ftp.cwd(source)
    filelist=ftp.nlst()
    for file in filelist:
        if ((file.endswith("xml.gz") | file.endswith("md5")) & (file not in files_downloaded)):
            if(file.endswith("xml.gz")):
                index = len(df.index) + 1
                df.at[index,'retrieval']="pending"
                df.at[index,'name']=file
                df.at[index,'folder']=folder_name
                #ftp.retrbinary("RETR "+file, open(os.path.join(work_dir,file),"wb").write)
                print file + " downloaded"
                df.at[index,'date']=str(datetime.now().date())
                df.at[index,'time']=str(datetime.now().time())
                df.at[index,'retrieval']="complete"
                df.to_csv(result_file)
            else:
                #ftp.retrbinary("RETR "+file, open(os.path.join(work_dir,file),"wb").write)     
                print file + " downloaded" 
    df.to_csv(result_file)

    