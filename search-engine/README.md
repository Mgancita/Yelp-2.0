# Search-Engine
This project implements the search-service and web-app module for yelp 2.0 project as part of BIA-660 coursework

## Configure dataload and index config files.

### Mapping csv columns to tabel columns for dataload
	1. Update database configuration in below file.
		<Yelp2.0 directory>\search-engine\dataload\config\dataload-env.xml
		
	2. Map csv columns to tabel columns in below file.
		<Yelp2.0 directory>\search-engine\dataload\config\dataload.xml
		
### Mapping data import query from table to fields in index and search service query fields
	1. Update the import query for any customization in below file and map the result column to neccessary field 
	   name in index.
		<Yelp2.0 directory>\search-engine\index_config\config\dataimport.xml
	
	2. Update the query field in the below file to configure the list of index fields that needs to be queried 
	   when search REST service API is hit.
		<Yelp2.0 directory>\search-engine\search_service\conf\queryconf.xml
		
## Dataload, Indexing and Running Server.
1. cd <Yelp2.0 directory>\search-engine\search_service\setup\

2. Execute below DDL against the SQLITE database.<br/>
	$sqlite3 ..\db.sqlite3<br/>
	sqlite>.read yelp_2_DDL.sql<br/>
	Exit from sqlite prompt.

3. Activate virtual environment.<br/>
	$<Yelp2.0 directory>\search-engine\search_service\venv\Scripts\activation.bat
	
4. Load scraped and processed data from csv to database.<br/>
	$python <Yelp2.0 directory>\search-engine\dataload\script\dataload.py
	
5. Build index by importing data from database.<br/>
	$python <Yelp2.0 directory>\search-engine\dataload\script\dataload.py
	
6. Run server.<br/>
	$python <Yelp2.0 directory>\search-engine\search_service\manage.py runserver

	
Please refer [PROJECT SETUP](https://github.com/Mgancita/Yelp-2.0/blob/master/search-engine/PROJECT_SETUP.md "PROJECT_SETUP.md") for steps followed during project setup.
