[DISE Dashboard](https://dise.klp.org.in)
===============

Dashboard for Dise data to allow interactive dise data gathering

API Documentation - https://dise.klp.org.in/api/docs/

Deploying DISE dashboard
========================

DISE dashboard app still uses Python 2.7. Make sure to create a virtual environment with Python 2.x. Install requirements and then run the server using a standard systemctl gunicorn service.

Backing up and restoring database
---
This is what I do as of now. For backing up -

    pg_dump -Ox -h localhost -U klp klpdise_olap > klp/dise/backups/klpdise_olap-2013-11-08-0241-full.pgsql

For restoring the same -

    sudo psql -U klp -h localhost klpdise_olap < klpdise_olap-2013-11-08-0241-full.pgsql

Indicators
---

1. General
    - Rural
    - Urban
    - Government
    - Private

2. Facility (negatives only)
    - Without Pucca Building
    - Classrooms needing repair
    - Without Toilets
    - Without Girls Toilets
    - Without Electricity
    - Without Secure Wall
    - Without Mid-Day-Meal
    - Without Drinking Water
    - Without Medical Checkup
    - Without Library
    - Without Blackboard
    - Without Playground
    - Without Ramps

3. Teachers
    - Without separate room for HM
    - Without HM

4. RTE
    - Without SDMC Constituted
    - Without SDMC Meetings
    - Without Text Books
    - With Children from Weaker Section Enrolled (PVT only)

5. Compound Indicators
    - With enrolment < 25
    - With PTR > 35
    - With Girls:Boys Gender ratio < 1

6. Range Indicators
    - With the number of class rooms between [___] and [___]
    - With the number of Teacher between [___] and [___]
    - With number of girls in class [____] between [____] and [____]
    - With number of boys in class [____] between [____] and [____]
