# Search-Engine
This project implements the search engine module for yelp 2.0 project as part of BIA-660 coursework

## Configure dataload and index config files.

### Mapping csv columns to tabel columns for dataload
	1. Update database configuration in below file.
		<Yelp2.0 donwload directory>\search-engine\dataload\config\dataload-env.xml
		
	2. Map csv columns to tabel columns in below file.
		<Yelp2.0 donwload directory>\search-engine\dataload\config\dataload.xml
		
### Mapping data import query from table to fields in index.
	1. Update the import query for any customization in below file and map the result column to neccessary field 
	   name in index.
		<Yelp2.0 donwload directory>\search-engine\index_config\config\dataimport.xml
	
	2. Update the query field in the below file to configure the list of index fields that needs to be queried 
	   when search REST service API is hit.
		<Yelp2.0 donwload directory>\search-engine\search_service\conf\queryconf.xml
		
## Execution of jobs and start server.
1. cd <Yelp2.0 donwload directory>

2. Activate virtual environment.
	$.\search-engine\search_service\venv\Scripts\activation.bat
	
3. Load scraped and processed data from csv to database.
	$python .\search-engine\dataload\script\dataload.py
	
4. Build index by importing data from database.
	$python .\search-engine\dataload\script\dataload.py
	
5. Run server.
	$python .\search-engine\search_service\manage.py runserver

	
Please refer PROJECT_SETUP.md for steps followed during project setup.