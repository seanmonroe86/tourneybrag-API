Packages used:
	Python 3
	PostgreSQL
	Django
	Apache


Steps to run this backend as used by the project:

DATABASE:
Install PostgreSQL.
Create a user and database for use by Tourneybrag. You can use this using
PGAdmin that comes with PostgreSQL when installing PostgreSQL.
SERVER:
Install Apache.
Create two virtual host confs:
	tourneybrag.conf - enable a ProxyPass to the anticipated Node server's port.
	django.conf - enable a ProxyPass to the anticipated Django server's port.
Include the confs in the httpd.conf file and restart the server.


DJANGO:
Install Django.
Change mysite/settings.py to reflect the database's settings.
Run:
	python manage.py makemigrations && python manage.py migrate



