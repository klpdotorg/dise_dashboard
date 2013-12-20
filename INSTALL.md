DISE Dashboard Setup Guide
===============

Here are the steps you need to follow(on Debian/Ubuntu/Mint) to get this up and running -

1. Obtain the database dump
2. Install PostgreSQL, create a user and make it `SUPERUSER`(needed for creating functions and extensions)
3. extract the database dump(if it's compressed) and restore it -

        psql -h localhost -U username dbname < klp-dump-filename.pgsql

4. clone this repository
5. create a `virtualenv` and activate it
6. install the required packages -

        pip install -r requirements.txt

7. create a local settings file -

        cp dise_dashboard/local_settings.sample.py dise_dashboard/local_settings.py

8. edit the file `local_settings.py` and put in the database details (Postgres 9.3 + PostGIS 2.1)
9. run the server

        python manage.py runserver <port>

10. Open your browser and test if it's working.