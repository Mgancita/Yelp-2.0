## Project setup steps followed as below:
This page contains the steps followed during the project setup.

1. This project was implemented in below python version.  
$python  
Python 3.7.0 (default, Jun 28 2018, 08:04:48) [MSC v.1912 64 bit (AMD64)] :: Anaconda, Inc. on win32  
Type "help", "copyright", "credits" or "license" for more information.  

2. Create the project directory  
$mkdir search_service && cd search_service  
 
3. creates virtual enviroment named venv  
search_service$ virtualenv --python=python3 venv search_service  

4. Activate the virtual enviroment named venv  
virtualenv --python=python3 venv  
Windows:  
virtualenv --python=<python_installed_directory>\python.exe venv  

5. Activate virtual enviroment  
activate venv  


6. Install packages 
		Install Django  
			pip install Django==2.0.3  

		Install djangorestframework  
			pip install djangorestframework  
		
		Install xmltodict 0.12.0
			pip install xmltodict
        
        Install pandas-0.24.2
            pip install pandas
        
        Install nltk-3.4.1
            pip install nltk
        
        Install stemming-1.0.1
            pip install stemming

8. Create django project.  
django-admin.py startproject api .  


9. Create django app  
django-admin.py startapp search  

django-admin.py startapp webapp


10. Sync database for the first time and create an initial user and set password for that user  
python manage.py migrate  

11. Execute below command with necessary user name and password  
python manage.py createsuperuser --email admin@example.com --username admin  

12. Create search-engine/search/urls.py  & search-engine/search/webapp/urls.py
	a. Add below code snippet  
		urlpatterns = [
			path('search/', views.search_index)
		]
	b. Add below snippet in search-engine/search/webapp/urls.py
		urlpatterns = [
			path('', views.webapp_home)
		]
	b. update url pattern redirections in api/urls.py
		urlpatterns = [
			path('admin/', admin.site.urls),
			re_path('api/', include('search.urls')),
			re_path('yelp/', include('webapp.urls')),
			url('^(admin|api|yelp)/', admin.site.urls)
		]
13. Excecute below command.  
python manage.py makemigrations  

14. Execute below command.  
python manage.py migrate  
 
15. Execute below command.  
python manage.py makemigrations  

16. Excecute below command.
python manage.py migrate

17. Execute below command to test.  
python manage.py test  

18. Execute below command to start the search server.  
python manage.py runserver  