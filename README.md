Packages used:
	Python 3
	PostgreSQL
	Django
	Apache


Steps to run this backend as used by the project:

SERVER:
Install Apache.
Include the two sample virtual host configs in Apache's httpd.conf file.


DATABASE:
Install PostgreSQL and optionally PGAdmin.
Create a user and database for use by Tourneybrag.
Values for the username, password, database name and service port used in this
project are found in mysite/settings.py.


API:
Install Django.
This project was started in the course of following the official tutorial. This
means the project name is 'mysite', and the application name is 'tourneyBrag'.

Change mysite/settings.py to reflect the database's settings, if different from
those of this project.

Run:
	python manage.py makemigrations && python manage.py migrate

This will create the database relations required by tourneyBrag automatically.

FINISH:
Apache, Django and PostgreSQL must be running. Django's queries will be
directed toward the database in its settings.py file. Apache will rpxy all HTTP
requests to the Node and Django services running on the machine.

OPTIONAL:
A domain name (sean-monroe.com) is used for this project in addition to CNAMEs
'django' and 'tourneybrag'. A single IP address is sufficient, but this will
cause trouble with Apache's vhost configurations.

ADDITIONAL NOTES:
The server is run on an Arch Linux system. All but Django's installations,
setup and configurations were done using the Arch Wiki for instructions, in
addition to their documentation. The instructions here are a bit short and
high-level, because the documentation followed by our team is better than
anything that can be typed in this document.

One more thing: this server is also secured with TLS. The provided Apache
virtual host configurations direct unsecured HTTP requests go to the server
while in practice they redirect requests to HTTPS requests. The methods used to
obtain signed certificates are much too tedious and HTTP requests to port 80
suffice; hashed passwords have not been implemented yet, so security is hardly
a concern.

Instructions used in developing backend:
Django: https://docs.djangoproject.com/en/1.10/intro/tutorial01/
Apache: https://wiki.archlinux.org/index.php/Apache_HTTP_Server
PostgreSQL: https://wiki.archlinux.org/index.php/PostgreSQL


