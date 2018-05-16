Pubmed Retrieval 
========================

This library is a basic download/update of the PubMed database into a working directory.  

Every time that is executed, the library search for new updates in the ftp://ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/ and download into a working directory.  
Mantains all the history in a csv update_history file that contains all the updates downloaded to control actualizations.
  
If it's executed for the first time the library will download all the baseline of PubMed database (ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/) and after that it will 
download all the actualizations of the current year ftp://ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/

Every time that it's executed will validate if new updates are releases into the updatefiles folder of the PubMed ftp.

The tool only download the files that contains the contents of the documents, that is files *.xml.gz

This library can be use as a step of a pipeline with the objective of mantain updated the PubMed Data to continue with the next processing.

========================

1.- Clone this repository 

    $ git clone https://github.com/javicorvi/pubmed_update.git
    
2.- Python 2.7 
	
	
3.- Third Party 
	
	The pandas library: pip install pandas
	
4.- Run the script
	
	To run the script just execute python pubmed_update -o /home/myname/pubmed_data 

5.- The container 
	
	If you just want to run the app without any kind of configuration you can do it 
	through the docker container is avaiblable in https://hub.docker.com/r/javidocker/pubmed_update/ 

	To run the docker: 
	
	docker run --rm -u $UID  -v /home/yourname/pubmed_data:/app/data pubmed_update

	the path home/yourname/pubmed_data will be the working directory in where the data will be downloaded
