# Search-Engine
This project implements the search engine module for yelp 2.0 project as part of BIA-660 coursework

## Mapping csv columns to tabel columns for dataload
	a. Update database configuration in below file.
		search-engine\dataload\config\dataload-env.xml
		
	b. Map csv columns to tabel columns in below file.
		search-engine\dataload\config\dataload.xml
		
## Mapping data import query from table to fields in index.
		\search-engine\index_config\config\dataimport.xml
		
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

	