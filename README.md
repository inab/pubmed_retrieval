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

    $ git clone https://github.com/javicorvi/pubmed_retrieval.git
    
2.- Python 2.7 
	
	
3.- Third Party 
	
	pip install pandas
	pip install SQLAlchemy

4.- Sqlite 
	
	To control the updates of pubmed a sqlite database is generated to store the already downloaded files.  
	The script for the creation are inside the project: db/dll_creation.sql as well as an empty database ready to use: db/bio_databases.db.
	 
	The database has to be manually generated or copy; 
	
5.- Run the script
	
	To run the script just execute python pubmed_retrieval -p /home/myuser/config.properties
	
	The config.properties file contains the parameters for the execution
	
	[MAIN]
	output=/home/myuser/your_work_dir/pubmed_data/
	[DATABASE]
	url=sqlite:////home/yourname/your_work_dir/bio_databases.db
	
	To pass parameters individually:
	-o ----- > Output Directory
	-u ------> SQLITE Database URL
	
	Remember to generate the database in home/yourname/your_work_dir/ 
	
6.- The container 
	
	If you just want to run the app without any kind of configuration you can do it 
	through the docker container is avaiblable in https://hub.docker.com/r/inab/pubmed_retrieval/ 

	The path home/yourname/your_work_dir will be the working directory in where the data will be downloaded, this is the configuration of a 
	Volumes for store the data outside of the container.

	To run the docker: 
	
	1)  Wiht the default parameters: 
	    
	    docker run --rm -u $UID  -v /home/yourname/your_work_dir/:/app/data pubmed_retrieval python pubmed_retrieval.py -p config.properties

		The default config.properties its inside the container and has the following default parameters: 
		
		[MAIN]
		output=/app/data/pubmed_data/
		[DATABASE]
		url=sqlite:////app/data/bio_databases.db
	
		It's the most basic configuration, and it 's recommended to used in this way.
	
	2)  Passing specific parameters:
	
		docker run --rm -u $UID  -v /home/yourname/your_work_dir/:/app/data pubmed_retrieval python pubmed_retrieval.py -u sqlite:////app/data/bio_databases.db -o /app/data/pubmed_data/

	3) Passing specifig config.properties file:
	
		Put your own config file in the your working directory:  /home/yourname/your_work_dir/config.properties  
		
		docker run --rm -u $UID  -v /home/yourname/your_work_dir/:/app/data pubmed_retrieval python pubmed_retrieval.py -p /app/data/config_own.properties
		
		
